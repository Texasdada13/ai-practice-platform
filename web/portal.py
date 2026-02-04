"""
Client Portal Blueprint for AI Practice Platform.

Provides a dedicated branded portal experience for organization clients.
"""

import json
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from database import db, User, Organization, Assessment

portal_bp = Blueprint('portal', __name__, url_prefix='/portal')


def get_organization_by_slug(slug):
    """Get organization by slug."""
    return Organization.query.filter_by(slug=slug, status='active').first()


def portal_login_required(f):
    """Decorator to require login and valid organization."""
    @wraps(f)
    def decorated_function(org_slug, *args, **kwargs):
        org = get_organization_by_slug(org_slug)
        if not org:
            flash('Organization not found.', 'danger')
            return redirect(url_for('index'))

        if not current_user.is_authenticated:
            return redirect(url_for('portal.portal_login', org_slug=org_slug))

        if current_user.organization_id != org.id:
            flash('You do not have access to this portal.', 'danger')
            logout_user()
            return redirect(url_for('portal.portal_login', org_slug=org_slug))

        return f(org_slug, org=org, *args, **kwargs)
    return decorated_function


# =============================================================================
# Portal Authentication Routes
# =============================================================================

@portal_bp.route('/<org_slug>')
@portal_bp.route('/<org_slug>/login', methods=['GET', 'POST'])
def portal_login(org_slug):
    """Client portal login page."""
    org = get_organization_by_slug(org_slug)
    if not org:
        flash('Organization not found.', 'danger')
        return redirect(url_for('index'))

    # If already logged in and belongs to this org, redirect to dashboard
    if current_user.is_authenticated:
        if current_user.organization_id == org.id:
            return redirect(url_for('portal.portal_dashboard', org_slug=org_slug))
        else:
            logout_user()

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == '1'

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Verify user belongs to this organization
            if user.organization_id != org.id:
                flash('You do not have access to this portal.', 'danger')
                return render_template('portal/login.html', org=org)

            if not user.is_active:
                flash('Your account has been deactivated.', 'danger')
                return render_template('portal/login.html', org=org)

            login_user(user, remember=remember)

            # Set session variables
            session['organization_id'] = org.id
            session['organization'] = org.name
            session['portal_slug'] = org_slug

            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('portal.portal_dashboard', org_slug=org_slug))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('portal/login.html', org=org)


@portal_bp.route('/<org_slug>/logout')
def portal_logout(org_slug):
    """Client portal logout."""
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('portal.portal_login', org_slug=org_slug))


# =============================================================================
# Portal Dashboard Routes
# =============================================================================

@portal_bp.route('/<org_slug>/dashboard')
@login_required
@portal_login_required
def portal_dashboard(org_slug, org=None):
    """Client portal dashboard."""
    # Get latest assessment
    latest_assessment = Assessment.query.filter_by(
        organization_id=org.id
    ).order_by(Assessment.created_at.desc()).first()

    # Extract data from latest assessment
    assessment_data = None
    dimension_scores = {}
    dimension_labels = []
    dimension_values = []
    strengths = []
    recommendations = []

    if latest_assessment and latest_assessment.result:
        result = latest_assessment.result
        assessment_data = {
            'overall_score': result.get('overall_score', 0),
            'maturity_level': result.get('maturity_level', 'Exploring'),
            'created_at': latest_assessment.created_at
        }

        dimension_scores = result.get('dimension_scores', {})
        for dim_id, dim_info in dimension_scores.items():
            dim_name = dim_info.get('name', dim_id.replace('_', ' ').title())
            dimension_labels.append(dim_name)
            dimension_values.append(dim_info.get('score', 0))

        strengths = result.get('strengths', [])

        # Extract recommendations
        raw_recs = result.get('recommendations', [])
        for rec in raw_recs[:5]:
            if isinstance(rec, dict):
                recommendations.append(rec.get('text', rec.get('recommendation', str(rec))))
            else:
                recommendations.append(str(rec))

    return render_template(
        'portal/dashboard.html',
        org=org,
        latest_assessment=assessment_data,
        dimension_scores=dimension_scores,
        dimension_labels=json.dumps(dimension_labels),
        dimension_values=json.dumps(dimension_values),
        strengths=strengths,
        recommendations=recommendations,
        now=datetime.now()
    )


@portal_bp.route('/<org_slug>/assessments')
@login_required
@portal_login_required
def portal_assessments(org_slug, org=None):
    """Client portal assessment history."""
    assessments = Assessment.query.filter_by(
        organization_id=org.id
    ).order_by(Assessment.created_at.desc()).all()

    # Process assessments
    assessment_list = []
    prev_score = None

    for a in reversed(assessments):
        if a.result and 'overall_score' in a.result:
            score = a.result.get('overall_score', 0)
            maturity = a.result.get('maturity_level', 'Exploring')
            score_change = score - prev_score if prev_score is not None else None

            assessment_list.insert(0, {
                'id': a.id,
                'overall_score': score,
                'maturity_level': maturity,
                'score_change': score_change,
                'created_at': a.created_at
            })
            prev_score = score

    # Chart data
    chart_labels = [a['created_at'].strftime('%b %d') if a['created_at'] else '' for a in reversed(assessment_list)]
    chart_scores = [a['overall_score'] for a in reversed(assessment_list)]

    return render_template(
        'portal/assessments.html',
        org=org,
        assessments=assessment_list,
        chart_labels=json.dumps(chart_labels),
        chart_scores=json.dumps(chart_scores),
        now=datetime.now()
    )


@portal_bp.route('/<org_slug>/assessment/new')
@login_required
@portal_login_required
def portal_new_assessment(org_slug, org=None):
    """Start a new assessment from portal."""
    # Set up session for assessment
    session['organization_id'] = org.id
    session['organization'] = org.name
    session['sector'] = org.sector
    session['portal_slug'] = org_slug
    session['from_portal'] = True

    # Redirect to main assessment flow
    return redirect(url_for('assessment'))


@portal_bp.route('/<org_slug>/chat')
@login_required
@portal_login_required
def portal_chat(org_slug, org=None):
    """Client portal AI chat."""
    # Set up session
    session['organization_id'] = org.id
    session['organization'] = org.name
    session['portal_slug'] = org_slug

    # Redirect to main chat with portal context
    return redirect(url_for('chat_page'))


@portal_bp.route('/<org_slug>/documents')
@login_required
@portal_login_required
def portal_documents(org_slug, org=None):
    """Client portal documents."""
    session['portal_slug'] = org_slug
    return redirect(url_for('documents_page'))


@portal_bp.route('/<org_slug>/profile')
@login_required
@portal_login_required
def portal_profile(org_slug, org=None):
    """Client portal profile page."""
    return render_template(
        'portal/profile.html',
        org=org,
        now=datetime.now()
    )


@portal_bp.route('/<org_slug>/export/pdf')
@login_required
@portal_login_required
def portal_export_pdf(org_slug, org=None):
    """Export latest assessment as PDF from portal."""
    # Get latest assessment
    latest_assessment = Assessment.query.filter_by(
        organization_id=org.id
    ).order_by(Assessment.created_at.desc()).first()

    if not latest_assessment:
        flash('No assessment found to export.', 'warning')
        return redirect(url_for('portal.portal_dashboard', org_slug=org_slug))

    # Redirect to export route with assessment ID
    return redirect(url_for('export_assessment_pdf', assessment_id=latest_assessment.id))
