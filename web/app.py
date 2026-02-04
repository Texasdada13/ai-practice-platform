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
import re
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, send_file
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Add src and web to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import exceptions and validators
from exceptions import (
    PlatformException, ValidationError, AssessmentNotFoundError,
    NoActiveAssessmentError, NoChatSessionError, DocumentNotFoundError
)
from validators import (
    validate_lead_data, validate_chat_message, validate_assessment_responses,
    validate_sector, validate_uuid, sanitize_string
)

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
from frameworks.mlops_builder import MLOpsFrameworkBuilder
from frameworks.data_strategy_builder import DataStrategyBuilder

# Import roadmap modules
from roadmap.roadmap_engine import AIRoadmapEngine, RoadmapHorizon
from roadmap.use_case_prioritizer import UseCasePrioritizer

# Import utility modules
from utils.document_export import get_document_exporter

# Import database modules
from database import db, init_db, Lead, Assessment, ChatSession, Document
from database.models import User, Organization, Role, AuditLog, create_audit_log, Permissions
from database.repository import (
    LeadRepository, AssessmentRepository, ChatSessionRepository, DocumentRepository
)

# Import authentication modules
from web.auth import auth_bp, init_login_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_action(action: str, resource_type: str = None, resource_id: str = None, details: dict = None):
    """Helper function to log user actions for audit trail."""
    from flask_login import current_user
    try:
        user_id = current_user.id if current_user and current_user.is_authenticated else None
        org_id = current_user.organization_id if current_user and current_user.is_authenticated else None
        create_audit_log(
            action=action,
            user_id=user_id,
            organization_id=org_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string[:500] if request and request.user_agent else None
        )
        db.session.commit()
    except Exception as e:
        logger.warning(f"Failed to create audit log: {e}")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-practice-platform-2024-secure')

# Database configuration
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "data", "platform.db")}')

# Ensure data directory exists
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize database
init_db(app)

# Initialize Flask-Login
init_login_manager(app)

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Security: CSRF Protection
csrf = CSRFProtect(app)

# Security: Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-CSRFToken"]
    }
})

# Configure CSRF to skip checking for API routes
# API routes will use session-based auth; in production use proper API tokens
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

@app.before_request
def csrf_protect():
    """Apply CSRF protection only to non-API routes"""
    # Skip CSRF in testing mode
    if app.config.get('TESTING') or app.config.get('WTF_CSRF_ENABLED') == False:
        return
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        if not request.path.startswith('/api/'):
            csrf.protect()

# In-memory cache for active chat sessions (database is primary storage)
# Chat session objects from chat_engine need to stay in memory during active conversations
chat_sessions_cache: Dict[str, Any] = {}

# Legacy in-memory storage (kept for backward compatibility during migration)
# These will be phased out as database adoption completes
assessments_db: Dict[str, Dict[str, Any]] = {}
leads_db: Dict[str, Dict[str, Any]] = {}
chat_sessions_db: Dict[str, Any] = {}
documents_db: Dict[str, Any] = {}

# Initialize engines
strategy_builder = AIStrategyBuilder()
governance_builder = GovernanceFrameworkBuilder()
ethics_builder = EthicsFrameworkBuilder()
mlops_builder = MLOpsFrameworkBuilder()
data_strategy_builder = DataStrategyBuilder()


# =============================================================================
# BRANDING CONTEXT PROCESSOR
# =============================================================================

# Default Patriot Tech branding
DEFAULT_BRANDING = {
    'name': 'AI Practice Platform',
    'logo_url': '/static/images/patriot-logo.svg',
    'primary_color': '#0066FF',
    'secondary_color': '#00D4AA',
    'powered_by': 'Patriot Tech Systems Consulting LLC',
    'powered_by_url': 'https://www.patriottechsystems.com'
}


@app.context_processor
def inject_branding():
    """Inject branding variables into all templates."""
    from flask_login import current_user

    branding = DEFAULT_BRANDING.copy()

    # If user is logged in and has an organization, use their branding
    if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        org = current_user.organization
        if org:
            # Only apply custom branding for professional/enterprise plans
            if org.plan in ['professional', 'enterprise']:
                if org.logo_url:
                    branding['logo_url'] = org.logo_url
                if org.primary_color:
                    branding['primary_color'] = org.primary_color
                if org.secondary_color:
                    branding['secondary_color'] = org.secondary_color
                branding['name'] = org.name
            else:
                # Starter plan: just show org name but keep Patriot branding
                branding['name'] = org.name

    return {'branding': branding}
roadmap_engine = AIRoadmapEngine()
use_case_prioritizer = UseCasePrioritizer()


# =============================================================================
# ROUTES - Main Pages
# =============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', sectors=SECTORS)


@app.route('/demo')
def demo_mode():
    """
    Demo Mode - Skip assessment and explore all features with sample data.
    Creates a pre-populated session with realistic assessment results.
    """
    # Generate demo session IDs
    demo_assessment_id = f"demo-{uuid.uuid4().hex[:8]}"
    demo_lead_id = f"demo-lead-{uuid.uuid4().hex[:8]}"

    # Demo organization info
    demo_organization = "Demo Corporation"
    demo_sector = "financial_services"

    # Create realistic mock assessment result
    demo_result = {
        'assessment_id': demo_assessment_id,
        'organization_name': demo_organization,
        'overall_score': 62,
        'grade': 'B-',
        'maturity_level': 'Experimenting',
        'maturity_description': 'Your organization is actively experimenting with AI, running pilots and building foundational capabilities.',
        'dimension_scores': {
            'data_maturity': {
                'name': 'Data Maturity',
                'score': 58,
                'max_score': 100,
                'grade': 'C+',
                'maturity_level': 'Developing',
                'interpretation': 'Data capabilities are emerging but need strengthening'
            },
            'technology_infrastructure': {
                'name': 'Technology Infrastructure',
                'score': 71,
                'max_score': 100,
                'grade': 'B',
                'maturity_level': 'Established',
                'interpretation': 'Solid technical foundation for AI initiatives'
            },
            'process_operations': {
                'name': 'Process & Operations',
                'score': 55,
                'max_score': 100,
                'grade': 'C',
                'maturity_level': 'Developing',
                'interpretation': 'Processes need optimization for AI integration'
            },
            'workforce_culture': {
                'name': 'Workforce & Culture',
                'score': 68,
                'max_score': 100,
                'grade': 'B-',
                'maturity_level': 'Established',
                'interpretation': 'Good foundation for AI adoption culture'
            },
            'governance_compliance': {
                'name': 'Governance & Compliance',
                'score': 60,
                'max_score': 100,
                'grade': 'C+',
                'maturity_level': 'Developing',
                'interpretation': 'Governance framework needs enhancement'
            }
        },
        'top_strengths': [
            'Strong cloud infrastructure ready for AI workloads',
            'Leadership commitment to AI transformation',
            'Existing data science talent on team'
        ],
        'top_improvements': [
            'Establish formal AI governance framework',
            'Improve data quality and accessibility',
            'Develop AI ethics guidelines'
        ],
        'recommendations': [
            {
                'priority': 'High',
                'category': 'Governance',
                'title': 'Establish AI Governance Committee',
                'description': 'Form cross-functional team to oversee AI initiatives',
                'timeframe': '1-3 months'
            },
            {
                'priority': 'High',
                'category': 'Data',
                'title': 'Implement Data Quality Program',
                'description': 'Establish data quality metrics and monitoring',
                'timeframe': '3-6 months'
            },
            {
                'priority': 'Medium',
                'category': 'Process',
                'title': 'Pilot AI in Key Processes',
                'description': 'Identify 2-3 high-value processes for AI automation',
                'timeframe': '6-12 months'
            }
        ],
        'sector': demo_sector
    }

    # Store in assessments database
    assessments_db[demo_assessment_id] = {
        'id': demo_assessment_id,
        'lead_id': demo_lead_id,
        'result': demo_result,
        'benchmark_comparison': {
            'overall': {
                'score': 62,
                'benchmark': 58,
                'percentile': 65,
                'comparison': 'above_average'
            },
            'dimensions': {}
        },
        'completed_at': datetime.now().isoformat(),
        'is_demo': True
    }

    # Store demo lead
    leads_db[demo_lead_id] = {
        'id': demo_lead_id,
        'name': 'Demo User',
        'email': 'demo@example.com',
        'organization': demo_organization,
        'title': 'AI Strategy Lead',
        'sector': demo_sector,
        'is_demo': True
    }

    # Set up session
    session['assessment_id'] = demo_assessment_id
    session['lead_id'] = demo_lead_id
    session['sector'] = demo_sector
    session['organization'] = demo_organization
    session['responses'] = {}  # Empty but present
    session['current_dimension'] = 5  # Mark as complete
    session['is_demo'] = True

    logger.info(f"Demo session started: {demo_assessment_id}")

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Main dashboard after assessment"""
    if 'assessment_id' not in session:
        return redirect(url_for('index'))

    assessment_id = session['assessment_id']

    # Try database first, fall back to in-memory
    assessment = AssessmentRepository.get_by_id(assessment_id)
    if assessment:
        assessment_data = assessment.to_dict()
    else:
        assessment_data = assessments_db.get(assessment_id, {})

    # If no assessment data found (e.g., server restarted and in-memory cleared),
    # redirect to index for demo mode or show error
    if not assessment_data or 'result' not in assessment_data:
        if session.get('is_demo'):
            # Re-trigger demo mode to regenerate data
            return redirect(url_for('demo_mode'))
        return redirect(url_for('index'))

    return render_template(
        'dashboard.html',
        assessment=assessment_data,
        organization=session.get('organization', 'Your Organization'),
        is_demo=session.get('is_demo', False)
    )


# =============================================================================
# ROUTES - Assessment History
# =============================================================================

@app.route('/history')
def assessment_history():
    """View assessment history and trends."""
    from flask_login import current_user

    # Get assessments for the current user/organization
    assessments = []
    chart_labels = []
    chart_scores = []

    if current_user and current_user.is_authenticated:
        # Get assessments from database for logged-in users
        org_assessments = Assessment.query.filter_by(
            organization_id=current_user.organization_id
        ).order_by(Assessment.created_at.desc()).all()

        prev_score = None
        for a in reversed(org_assessments):  # Oldest first for chart
            if a.result and 'overall_score' in a.result:
                score = a.result.get('overall_score', 0)
                maturity = a.result.get('maturity_level', 'Exploring')
                score_change = score - prev_score if prev_score is not None else None

                assessments.insert(0, {
                    'id': a.id,
                    'overall_score': score,
                    'maturity_level': maturity,
                    'score_change': score_change,
                    'created_at': a.created_at,
                    'result': a.result
                })
                chart_labels.append(a.created_at.strftime('%b %d') if a.created_at else '')
                chart_scores.append(score)
                prev_score = score

    # Get latest and previous for comparison
    latest_assessment = assessments[0] if assessments else None
    previous_assessment = assessments[1] if len(assessments) > 1 else None
    score_change = None

    if latest_assessment and previous_assessment:
        score_change = latest_assessment['overall_score'] - previous_assessment['overall_score']

    # Dimension comparison data
    dimension_comparison = False
    dimension_labels = []
    current_dimensions = []
    previous_dimensions = []

    if latest_assessment and previous_assessment:
        latest_dims = latest_assessment.get('result', {}).get('dimension_scores', {})
        prev_dims = previous_assessment.get('result', {}).get('dimension_scores', {})

        if latest_dims and prev_dims:
            dimension_comparison = True
            for dim_id, dim_data in latest_dims.items():
                dim_name = dim_data.get('name', dim_id.replace('_', ' ').title())
                dimension_labels.append(dim_name)
                current_dimensions.append(dim_data.get('score', 0))
                prev_dim = prev_dims.get(dim_id, {})
                previous_dimensions.append(prev_dim.get('score', 0))

    return render_template(
        'history.html',
        assessments=assessments,
        latest_assessment=latest_assessment,
        previous_assessment=previous_assessment,
        score_change=score_change,
        chart_labels=json.dumps(chart_labels),
        chart_scores=json.dumps(chart_scores),
        dimension_comparison=dimension_comparison,
        dimension_labels=json.dumps(dimension_labels),
        current_dimensions=json.dumps(current_dimensions),
        previous_dimensions=json.dumps(previous_dimensions)
    )


@app.route('/assessment/<assessment_id>/view')
def view_assessment(assessment_id):
    """View a specific assessment."""
    from flask_login import current_user

    # Try database first
    assessment = AssessmentRepository.get_by_id(assessment_id)

    if not assessment:
        # Try in-memory
        assessment_data = assessments_db.get(assessment_id)
        if not assessment_data:
            return render_template('error.html', error='Assessment not found'), 404
    else:
        assessment_data = assessment.to_dict()

    # Security check - only allow viewing own org's assessments
    if current_user and current_user.is_authenticated:
        if assessment and assessment.organization_id != current_user.organization_id:
            return render_template('error.html', error='Access denied'), 403

    return render_template(
        'results.html',
        result=assessment_data.get('result', {}),
        benchmark={},
        comparison={},
        sector=assessment_data.get('sector', 'general'),
        viewing_history=True
    )


@app.route('/export/assessment')
@app.route('/export/assessment/<assessment_id>')
def export_assessment_pdf(assessment_id=None):
    """Export assessment as branded PDF."""
    from flask_login import current_user
    from utils.document_export import get_assessment_exporter

    # Get assessment data
    if assessment_id:
        # Export specific assessment
        assessment = AssessmentRepository.get_by_id(assessment_id)
        if not assessment:
            return jsonify({'error': 'Assessment not found'}), 404
        assessment_data = assessment.to_dict()

        # Security check
        if current_user and current_user.is_authenticated:
            if assessment.organization_id != current_user.organization_id:
                return jsonify({'error': 'Access denied'}), 403
    else:
        # Export current session assessment
        assessment_id = session.get('assessment_id')
        if not assessment_id:
            return jsonify({'error': 'No assessment in session'}), 400

        # Try database first
        assessment = AssessmentRepository.get_by_id(assessment_id)
        if assessment:
            assessment_data = assessment.to_dict()
        else:
            # Try in-memory
            assessment_data = assessments_db.get(assessment_id)
            if not assessment_data:
                return jsonify({'error': 'Assessment not found'}), 404

    # Get branding (use organization's branding if logged in, else default)
    branding = DEFAULT_BRANDING.copy()
    organization_name = session.get('organization', 'Organization')

    if current_user and current_user.is_authenticated and current_user.organization:
        org = current_user.organization
        organization_name = org.name
        branding.update({
            'name': org.name if org.name else branding['name'],
            'primary_color': org.primary_color or branding['primary_color'],
            'secondary_color': org.secondary_color or branding['secondary_color'],
            'powered_by': DEFAULT_BRANDING['powered_by'],
        })

    # Generate PDF
    try:
        exporter = get_assessment_exporter()
        pdf_buffer = exporter.export(
            assessment_data=assessment_data,
            branding=branding,
            organization_name=organization_name
        )

        # Create filename
        date_str = datetime.now().strftime('%Y%m%d')
        safe_org = re.sub(r'[^\w\s-]', '', organization_name).strip().replace(' ', '_')
        filename = f"AI_Assessment_{safe_org}_{date_str}.pdf"

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error exporting assessment PDF: {e}")
        return jsonify({'error': 'Failed to export PDF'}), 500


# =============================================================================
# ROUTES - Assessment
# =============================================================================

@app.route('/start', methods=['POST'])
@limiter.limit("10 per minute")
def start_assessment():
    """Start a new assessment after lead capture"""
    try:
        # Validate and sanitize all form inputs
        validated_data = validate_lead_data(request.form)

        # Create lead in database
        lead = LeadRepository.create(
            name=validated_data['name'],
            email=validated_data['email'],
            organization=validated_data['organization'],
            title=validated_data['title'],
            sector=validated_data['sector']
        )

        # Create assessment in database
        assessment = AssessmentRepository.create(
            lead_id=lead.id,
            sector=validated_data['sector'],
            status='in_progress'
        )

        # Also store in legacy in-memory for backward compatibility
        lead_data = lead.to_dict()
        leads_db[lead.id] = lead_data

        # Set up session
        session['assessment_id'] = assessment.id
        session['lead_id'] = lead.id
        session['sector'] = validated_data['sector']
        session['organization'] = validated_data['organization']
        session['responses'] = {}
        session['current_dimension'] = 0

        # Audit log for assessment creation
        log_action('assessment.create', 'assessment', assessment.id,
                   {'sector': validated_data['sector'], 'organization': validated_data['organization']})

        logger.info(f"Assessment started: {assessment.id} for {validated_data['organization']}")
        return redirect(url_for('assessment'))

    except ValidationError as e:
        logger.warning(f"Validation error in start_assessment: {e.message}")
        return render_template('index.html', sectors=SECTORS, error=e.message), 400


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
@limiter.limit("30 per minute")
def submit_dimension():
    """Submit responses for a dimension and move to next"""
    if 'assessment_id' not in session:
        return jsonify({'error': 'No active assessment', 'code': 'NO_ACTIVE_ASSESSMENT'}), 400

    try:
        data = request.json or {}
        responses = data.get('responses', {})

        # Validate responses
        validated_responses = validate_assessment_responses(responses)

        current_responses = session.get('responses', {})
        current_responses.update(validated_responses)
        session['responses'] = current_responses
        session['current_dimension'] = session.get('current_dimension', 0) + 1

        sector = session.get('sector', 'general')
        questions = get_questions_for_sector(sector)

        if session['current_dimension'] >= len(questions):
            return jsonify({'redirect': url_for('results')})

        return jsonify({'redirect': url_for('assessment')})

    except ValidationError as e:
        logger.warning(f"Validation error in submit_dimension: {e.message}")
        return jsonify(e.to_dict()), 400


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

    # Ensure assessment has a result dict (for template compatibility)
    if 'result' not in assessment_data:
        assessment_data['result'] = {
            'overall_score': 0,
            'maturity_level': 'Exploring',
            'sector': session.get('sector', 'general')
        }

    return render_template(
        'chat.html',
        organization=session.get('organization', 'Your Organization'),
        assessment=assessment_data
    )


@app.route('/api/chat/start', methods=['POST'])
@limiter.limit("10 per minute")
def start_chat():
    """Start a new chat session"""
    try:
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

        # Safely get mode with fallback
        mode_str = data.get('mode', 'general')
        try:
            mode = ConversationMode(mode_str)
        except ValueError:
            mode = ConversationMode.GENERAL

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

    except Exception as e:
        import traceback
        logger.error(f"Error starting chat session: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Failed to start chat session: {str(e)}',
            'code': 'CHAT_START_ERROR',
            'details': str(e)
        }), 500


@app.route('/api/chat/message', methods=['POST'])
@limiter.limit("20 per minute")
def chat_message():
    """Send a chat message"""
    try:
        data = request.json or {}
        message = validate_chat_message(data.get('message', ''))
        chat_session_id = session.get('chat_session_id')

        if not chat_session_id:
            return jsonify({'error': 'No active chat session', 'code': 'NO_CHAT_SESSION'}), 400

        chat_engine = get_chat_engine()
        response = chat_engine.chat(chat_session_id, message)

        return jsonify(response)

    except ValidationError as e:
        return jsonify(e.to_dict()), 400
    except Exception as e:
        logger.error(f"Error in chat_message: {str(e)}")
        return jsonify({'error': 'An error occurred processing your message', 'code': 'CHAT_ERROR'}), 500


@app.route('/api/chat/stream', methods=['POST'])
@limiter.limit("20 per minute")
def chat_stream():
    """Stream a chat response using Server-Sent Events (SSE)."""
    try:
        data = request.json or {}
        message = validate_chat_message(data.get('message', ''))
        chat_session_id = session.get('chat_session_id')

        if not chat_session_id:
            return jsonify({'error': 'No active chat session', 'code': 'NO_CHAT_SESSION'}), 400

        def generate():
            """Generator for SSE stream."""
            chat_engine = get_chat_engine()

            for chunk in chat_engine.stream_chat(chat_session_id, message):
                # Format as SSE event
                event_type = chunk.get('type', 'token')
                if event_type == 'token':
                    # Send token content
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk['content']})}\n\n"
                elif event_type == 'done':
                    # Send completion event with suggested prompts
                    yield f"data: {json.dumps({'type': 'done', 'suggested_prompts': chunk.get('suggested_prompts', [])})}\n\n"
                elif event_type == 'error':
                    # Send error event
                    yield f"data: {json.dumps({'type': 'error', 'content': chunk['content']})}\n\n"

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'  # Disable buffering for nginx
            }
        )

    except ValidationError as e:
        return jsonify(e.to_dict()), 400
    except Exception as e:
        logger.error(f"Error in chat_stream: {str(e)}")
        return jsonify({'error': 'An error occurred', 'code': 'STREAM_ERROR'}), 500


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
@limiter.limit("10 per minute")
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

    log_action('framework.create', 'framework', None, {'type': 'strategy', 'sector': sector})
    return jsonify(strategy.to_dict())


@app.route('/api/frameworks/governance', methods=['POST'])
@limiter.limit("10 per minute")
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

    log_action('framework.create', 'framework', None, {'type': 'governance', 'sector': sector})
    return jsonify(framework.to_dict())


@app.route('/api/frameworks/ethics', methods=['POST'])
@limiter.limit("10 per minute")
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

    log_action('framework.create', 'framework', None, {'type': 'ethics', 'sector': sector})
    return jsonify(framework.to_dict())


@app.route('/api/frameworks/mlops', methods=['POST'])
@limiter.limit("10 per minute")
def generate_mlops():
    """Generate MLOps Framework"""
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_id = session.get('assessment_id')
    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    data = request.json or {}
    infrastructure = data.get('infrastructure_type', 'hybrid')
    cloud = data.get('primary_cloud', 'aws')

    framework = mlops_builder.build_framework(
        organization_name=organization,
        assessment_result=assessment_result,
        infrastructure_type=infrastructure,
        primary_cloud=cloud,
        team_size='medium'
    )

    log_action('framework.create', 'framework', None, {'type': 'mlops', 'infrastructure': infrastructure, 'cloud': cloud})
    return jsonify(framework.to_dict())


@app.route('/api/frameworks/data-strategy', methods=['POST'])
@limiter.limit("10 per minute")
def generate_data_strategy():
    """Generate Data Strategy Framework"""
    organization = session.get('organization', 'Organization')
    sector = session.get('sector', 'general')

    assessment_id = session.get('assessment_id')
    assessment_result = {}
    if assessment_id and assessment_id in assessments_db:
        assessment_result = assessments_db[assessment_id].get('result', {})

    data = request.json or {}
    cloud = data.get('primary_cloud', 'aws')

    framework = data_strategy_builder.build_framework(
        organization_name=organization,
        assessment_result=assessment_result,
        sector=sector,
        primary_cloud=cloud
    )

    log_action('framework.create', 'framework', None, {'type': 'data-strategy', 'sector': sector, 'cloud': cloud})
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
@limiter.limit("10 per minute")
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
@limiter.limit("5 per minute")
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

    # Audit log for document generation
    log_action('document.create', 'document', doc_id,
               {'doc_type': doc_type.value, 'word_count': document.word_count})

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
    """Download a generated document in specified format."""
    document = documents_db.get(doc_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    # Get requested format (default to markdown)
    format = request.args.get('format', 'markdown').lower()
    organization = session.get('organization', 'Organization')

    # Get markdown content
    markdown = document.to_markdown()

    if format == 'markdown' or format == 'md':
        return Response(
            markdown,
            mimetype='text/markdown',
            headers={'Content-Disposition': f'attachment; filename={document.doc_type.value}.md'}
        )

    # Use document exporter for other formats
    try:
        exporter = get_document_exporter()
        buffer = exporter.export(
            title=document.title,
            content=markdown,
            format=format,
            organization=organization
        )

        mime_type = exporter.get_mime_type(format)
        extension = exporter.get_extension(format)
        filename = f"{document.doc_type.value}{extension}"

        return Response(
            buffer.getvalue(),
            mimetype=mime_type,
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error exporting document: {e}")
        return jsonify({'error': 'Failed to export document'}), 500


@app.route('/api/documents/<doc_id>/export/<format>')
def export_document(doc_id, format):
    """Export a document to a specific format."""
    document = documents_db.get(doc_id)
    if not document:
        return jsonify({'error': 'Document not found'}), 404

    organization = session.get('organization', 'Organization')
    markdown = document.to_markdown()

    try:
        exporter = get_document_exporter()
        buffer = exporter.export(
            title=document.title,
            content=markdown,
            format=format.lower(),
            organization=organization
        )

        mime_type = exporter.get_mime_type(format)
        extension = exporter.get_extension(format)
        filename = f"{document.doc_type.value}{extension}"

        return Response(
            buffer.getvalue(),
            mimetype=mime_type,
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error exporting document: {e}")
        return jsonify({'error': 'Failed to export document'}), 500


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
@limiter.limit("10 per minute")
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
# Health Check & Monitoring
# =============================================================================

@app.route('/health')
@limiter.exempt
def health_check():
    """Health check endpoint for monitoring"""
    claude_status = "unknown"
    db_status = "unknown"

    try:
        claude = get_claude_client()
        claude_status = "available" if claude.is_available() else "unavailable"
    except Exception:
        claude_status = "error"

    # Check database connection
    try:
        assessment_stats = AssessmentRepository.get_stats()
        db_status = "connected"
    except Exception as e:
        db_status = "error"
        assessment_stats = {'total': 0, 'completed': 0, 'in_progress': 0}
        logger.error(f"Database health check failed: {e}")

    health_data = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'claude_api': claude_status,
            'database': db_status,
        },
        'stats': {
            'assessments_total': assessment_stats.get('total', 0),
            'assessments_completed': assessment_stats.get('completed', 0),
            'assessments_in_progress': assessment_stats.get('in_progress', 0),
            'active_chat_sessions': len(chat_sessions_cache),
            'leads_count': LeadRepository.count(),
            'documents_generated': DocumentRepository.count()
        }
    }

    return jsonify(health_data)


@app.route('/api/status')
@limiter.exempt
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'operational',
        'api_version': '1.0',
        'endpoints': {
            'assessment': '/api/assessment',
            'chat': '/api/chat',
            'frameworks': '/api/frameworks',
            'documents': '/api/documents',
            'roadmap': '/api/roadmap'
        }
    })


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle validation errors"""
    logger.warning(f"Validation error: {error.message}")
    return jsonify(error.to_dict()), 400


@app.errorhandler(PlatformException)
def handle_platform_error(error):
    """Handle platform-specific errors"""
    logger.error(f"Platform error: {error.message}")
    return jsonify(error.to_dict()), 500


@app.errorhandler(429)
def handle_rate_limit(error):
    """Handle rate limit exceeded"""
    logger.warning(f"Rate limit exceeded: {request.remote_addr}")
    return jsonify({
        'error': 'Rate limit exceeded. Please slow down.',
        'code': 'RATE_LIMIT_EXCEEDED'
    }), 429


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found', 'code': 'NOT_FOUND'}), 404
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {str(error)}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error', 'code': 'SERVER_ERROR'}), 500
    return render_template('error.html', error='Server error'), 500


# =============================================================================
# Run
# =============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3847))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug, port=port, host='0.0.0.0')
