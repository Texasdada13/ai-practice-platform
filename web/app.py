"""
AI Practice Platform - Unified Web Application

Flask-based web dashboard for:
- AI Readiness Assessment
- AI Chat Consultant (Claude-powered)
- Framework Generation
- Roadmap Planning
- Document Generation
"""

import os
import sys
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response
from flask_cors import CORS

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import assessment modules
from assessment.questions import get_questions_for_sector, SECTORS, get_question_count
from assessment.scoring import AIReadinessScorer, MaturityLevel
from assessment.benchmarks import get_benchmark_for_sector, compare_to_benchmark, get_benchmark_summary

# Import AI core modules
from ai_core.claude_client import ClaudeClient, get_claude_client
from ai_core.chat_engine import AIChatEngine, ConversationMode, get_chat_engine
from ai_core.document_generator import DocumentGenerator, DocumentType, get_document_generator

# Import framework modules
from frameworks.strategy_builder import AIStrategyBuilder
from frameworks.governance_builder import GovernanceFrameworkBuilder
from frameworks.ethics_framework import EthicsFrameworkBuilder

# Import roadmap modules
from roadmap.roadmap_engine import AIRoadmapEngine, RoadmapHorizon
from roadmap.use_case_prioritizer import UseCasePrioritizer

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-practice-platform-2024-secure')
CORS(app)

# In-memory storage (replace with database for production)
assessments_db = {}
leads_db = {}
chat_sessions_db = {}
documents_db = {}

# Initialize engines
strategy_builder = AIStrategyBuilder()
governance_builder = GovernanceFrameworkBuilder()
ethics_builder = EthicsFrameworkBuilder()
roadmap_engine = AIRoadmapEngine()
use_case_prioritizer = UseCasePrioritizer()


# =============================================================================
# ROUTES - Main Pages
# =============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', sectors=SECTORS)


@app.route('/dashboard')
def dashboard():
    """Main dashboard after assessment"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    assessment_id = session['assessment_id']
    assessment_data = assessments_db.get(assessment_id, {})

    return render_template(
        'dashboard.html',
        assessment=assessment_data,
        organization=session.get('organization', 'Your Organization')
    )


# =============================================================================
# ROUTES - Assessment
# =============================================================================

@app.route('/start', methods=['POST'])
def start_assessment():
    """Start a new assessment after lead capture"""
    lead_id = str(uuid.uuid4())
    lead_data = {
        'id': lead_id,
        'name': request.form.get('name', ''),
        'email': request.form.get('email', ''),
        'organization': request.form.get('organization', ''),
        'title': request.form.get('title', ''),
        'sector': request.form.get('sector', 'general'),
        'created_at': datetime.now().isoformat()
    }
    leads_db[lead_id] = lead_data

    # Create assessment session
    assessment_id = str(uuid.uuid4())
    session['assessment_id'] = assessment_id
    session['lead_id'] = lead_id
    session['sector'] = lead_data['sector']
    session['organization'] = lead_data['organization']
    session['responses'] = {}
    session['current_dimension'] = 0

    return redirect(url_for('assessment'))


@app.route('/assessment')
def assessment():
    """Assessment questionnaire page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    sector = session.get('sector', 'general')
    questions = get_questions_for_sector(sector)
    dimensions = list(questions.keys())
    current_dim_idx = session.get('current_dimension', 0)

    if current_dim_idx >= len(dimensions):
        return redirect(url_for('results'))

    current_dim = dimensions[current_dim_idx]
    dim_data = questions[current_dim]

    return render_template(
        'assessment.html',
        dimension=dim_data,
        dimension_id=current_dim,
        dimension_index=current_dim_idx,
        total_dimensions=len(dimensions),
        progress=int((current_dim_idx / len(dimensions)) * 100),
        sector=sector
    )


@app.route('/submit_dimension', methods=['POST'])
def submit_dimension():
    """Submit responses for a dimension and move to next"""
    if 'assessment_id' not in session:
        return jsonify({'error': 'No active assessment'}), 400

    data = request.json
    responses = data.get('responses', {})

    current_responses = session.get('responses', {})
    current_responses.update(responses)
    session['responses'] = current_responses
    session['current_dimension'] = session.get('current_dimension', 0) + 1

    sector = session.get('sector', 'general')
    questions = get_questions_for_sector(sector)

    if session['current_dimension'] >= len(questions):
        return jsonify({'redirect': url_for('results')})

    return jsonify({'redirect': url_for('assessment')})


@app.route('/results')
def results():
    """Display assessment results"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    responses = session.get('responses', {})
    sector = session.get('sector', 'general')
    organization = session.get('organization', 'Your Organization')

    # Score the assessment
    scorer = AIReadinessScorer(sector=sector)
    result = scorer.score_assessment(
        responses=responses,
        organization_name=organization,
        assessment_id=session['assessment_id']
    )

    # Get benchmark comparison
    benchmark_comparison = {}
    benchmark_summary = get_benchmark_summary(sector)

    benchmark_comparison['overall'] = compare_to_benchmark(
        result.overall_score, None, sector
    )

    benchmark_comparison['dimensions'] = {}
    for dim_id, dim_score in result.dimension_scores.items():
        benchmark_comparison['dimensions'][dim_id] = compare_to_benchmark(
            dim_score.score, dim_id, sector
        )

    # Store assessment result
    assessment_data = {
        'id': session['assessment_id'],
        'lead_id': session.get('lead_id'),
        'result': result.to_dict(),
        'benchmark_comparison': benchmark_comparison,
        'completed_at': datetime.now().isoformat()
    }
    assessments_db[session['assessment_id']] = assessment_data

    return render_template(
        'results.html',
        result=result,
        benchmark=benchmark_summary,
        comparison=benchmark_comparison,
        sector=sector
    )


# =============================================================================
# ROUTES - AI Chat
# =============================================================================

@app.route('/chat')
def chat_page():
    """AI Chat consultant page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    assessment_data = assessments_db.get(session['assessment_id'], {})

    return render_template(
        'chat.html',
        organization=session.get('organization', 'Your Organization'),
        assessment=assessment_data
    )


@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """Start a new chat session"""
    data = request.json or {}

    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')
    assessment_id = session.get('assessment_id')

    # Get assessment result if available
    assessment_result = None
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result')

    # Create chat session
    chat_engine = get_chat_engine()
    mode = ConversationMode(data.get('mode', 'general'))

    chat_session = chat_engine.create_session(
        organization_name=organization,
        sector=sector,
        assessment_result=assessment_result,
        mode=mode
    )

    session['chat_session_id'] = chat_session.session_id
    chat_sessions_db[chat_session.session_id] = chat_session

    return jsonify({
        'session_id': chat_session.session_id,
        'mode': mode.value,
        'suggested_prompts': chat_engine.get_suggested_prompts(chat_session.session_id)
    })


@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """Send a chat message"""
    data = request.json
    message = data.get('message', '')
    chat_session_id = session.get('chat_session_id')

    if not chat_session_id:
        return jsonify({'error': 'No active chat session'}), 400

    chat_engine = get_chat_engine()
    response = chat_engine.chat(chat_session_id, message)

    return jsonify(response)


@app.route('/api/chat/mode', methods=['POST'])
def change_chat_mode():
    """Change chat conversation mode"""
    data = request.json
    new_mode = data.get('mode', 'general')
    chat_session_id = session.get('chat_session_id')

    if not chat_session_id:
        return jsonify({'error': 'No active chat session'}), 400

    chat_engine = get_chat_engine()
    success = chat_engine.change_mode(chat_session_id, ConversationMode(new_mode))

    return jsonify({
        'success': success,
        'mode': new_mode,
        'suggested_prompts': chat_engine.get_suggested_prompts(chat_session_id)
    })


# =============================================================================
# ROUTES - Framework Generation
# =============================================================================

@app.route('/frameworks')
def frameworks_page():
    """Framework generation page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    return render_template(
        'frameworks.html',
        organization=session.get('organization', 'Your Organization')
    )


@app.route('/api/frameworks/strategy', methods=['POST'])
def generate_strategy():
    """Generate AI Strategy Framework"""
    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    strategy = strategy_builder.build_strategy(
        organization_name=organization,
        assessment_result=assessment_result,
        sector=sector
    )

    return jsonify(strategy.to_dict())


@app.route('/api/frameworks/governance', methods=['POST'])
def generate_governance():
    """Generate AI Governance Framework"""
    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    framework = governance_builder.build_framework(
        organization_name=organization,
        assessment_result=assessment_result,
        sector=sector
    )

    return jsonify(framework.to_dict())


@app.route('/api/frameworks/ethics', methods=['POST'])
def generate_ethics():
    """Generate AI Ethics Framework"""
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_id = session.get('assessment_id')
    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    framework = ethics_builder.build_framework(
        organization_name=organization,
        assessment_result=assessment_result,
        sector=sector
    )

    return jsonify(framework.to_dict())


# =============================================================================
# ROUTES - Roadmap
# =============================================================================

@app.route('/roadmap')
def roadmap_page():
    """Roadmap planning page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    return render_template(
        'roadmap.html',
        organization=session.get('organization', 'Your Organization')
    )


@app.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate AI Implementation Roadmap"""
    data = request.json or {}
    horizon = RoadmapHorizon(data.get('horizon', '18 months'))

    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')

    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    roadmap = roadmap_engine.generate_roadmap(
        organization_name=organization,
        assessment_result=assessment_result,
        horizon=horizon
    )

    return jsonify(roadmap.to_dict())


@app.route('/api/roadmap/gantt', methods=['GET'])
def get_gantt_data():
    """Get roadmap data for Gantt chart"""
    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')

    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    roadmap = roadmap_engine.generate_roadmap(
        organization_name=organization,
        assessment_result=assessment_result,
        horizon=RoadmapHorizon.MEDIUM
    )

    return jsonify(roadmap.to_gantt_data())


# =============================================================================
# ROUTES - Use Cases
# =============================================================================

@app.route('/use-cases')
def use_cases_page():
    """Use case prioritization page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    return render_template(
        'use_cases.html',
        organization=session.get('organization', 'Your Organization')
    )


@app.route('/api/use-cases/prioritize', methods=['POST'])
def prioritize_use_cases():
    """Prioritize AI use cases"""
    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    portfolio = use_case_prioritizer.prioritize(
        organization_name=organization,
        sector=sector,
        assessment_result=assessment_result
    )

    return jsonify(portfolio.to_dict())


# =============================================================================
# ROUTES - Document Generation
# =============================================================================

@app.route('/documents')
def documents_page():
    """Document generation page"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    doc_generator = get_document_generator()
    available_docs = doc_generator.get_available_documents()

    return render_template(
        'documents.html',
        organization=session.get('organization', 'Your Organization'),
        available_documents=available_docs
    )


@app.route('/api/documents/generate', methods=['POST'])
def generate_document():
    """Generate a document"""
    data = request.json
    doc_type = DocumentType(data.get('type', 'executive_summary'))
    custom_requirements = data.get('custom_requirements')

    assessment_id = session.get('assessment_id')
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_result = None
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result')

    doc_generator = get_document_generator()
    document = doc_generator.generate(
        doc_type=doc_type,
        organization_name=organization,
        assessment_result=assessment_result,
        sector=sector,
        custom_requirements=custom_requirements
    )

    # Store document
    doc_id = str(uuid.uuid4())
    documents_db[doc_id] = document

    return jsonify({
        'id': doc_id,
        'title': document.title,
        'content': document.content,
        'word_count': document.word_count,
        'sections': document.sections,
        'generated_at': document.generated_at.isoformat()
    })


@app.route('/api/documents/<doc_id>/download')
def download_document(doc_id):
    """Download a generated document"""
    document = documents_db.get(doc_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    markdown = document.to_markdown()

    return Response(
        markdown,
        mimetype='text/markdown',
        headers={'Content-Disposition': f'attachment; filename={document.doc_type.value}.md'}
    )


# =============================================================================
# API Routes - Assessment Data
# =============================================================================

@app.route('/api/assessment/<assessment_id>')
def get_assessment(assessment_id):
    """API endpoint to get assessment results"""
    if assessment_id in assessments_db:
        return jsonify(assessments_db[assessment_id])
    return jsonify({'error': 'Assessment not found'}), 404


@app.route('/api/questions/<sector>')
def get_questions(sector):
    """API endpoint to get questions for a sector"""
    questions = get_questions_for_sector(sector)
    return jsonify(questions)


@app.route('/api/benchmarks/<sector>')
def get_benchmarks(sector):
    """API endpoint to get benchmarks for a sector"""
    benchmark = get_benchmark_summary(sector)
    return jsonify(benchmark)


@app.route('/api/analysis/ai', methods=['POST'])
def get_ai_analysis():
    """Get Claude-powered analysis of assessment"""
    assessment_id = session.get('assessment_id')

    if not assessment_id or assessment_id not in assessments_db:
        return jsonify({'error': 'No assessment found'}), 400

    assessment_result = assessments_db[assessment_id].get('result')

    claude = get_claude_client()
    analysis = claude.analyze_assessment(assessment_result)

    return jsonify(analysis)


# =============================================================================
# Template Filters
# =============================================================================

@app.template_filter('format_score')
def format_score(value):
    """Format score for display"""
    return f"{value:.0f}"


@app.template_filter('score_color')
def score_color(value):
    """Get color based on score"""
    if value >= 76:
        return '#17a2b8'
    elif value >= 51:
        return '#28a745'
    elif value >= 26:
        return '#fd7e14'
    else:
        return '#dc3545'


@app.template_filter('maturity_icon')
def maturity_icon(maturity):
    """Get icon for maturity level"""
    icons = {
        'Exploring': 'search',
        'Experimenting': 'flask',
        'Scaling': 'trending-up',
        'Optimizing': 'rocket'
    }
    return icons.get(maturity, 'help-circle')


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error='Server error'), 500


# =============================================================================
# Run
# =============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3847))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, port=port, host='0.0.0.0')
