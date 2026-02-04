"""
Authentication Blueprint for AI Practice Platform.

Provides user registration, login, logout, and password management.
"""

import os
import re
import uuid
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from database import db, User, Organization, Role, AuditLog, create_audit_log, Permissions

# Allowed file extensions for logo upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def init_login_manager(app):
    """Initialize the login manager with the app."""
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(user_id)


# =============================================================================
# Decorators
# =============================================================================

def permission_required(permission):
    """Decorator to require specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            if not current_user.has_permission(permission):
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role."""
    return permission_required(Permissions.USER_MANAGE)(f)


def org_required(f):
    """Decorator to require organization membership."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.organization_id:
            flash('Please join or create an organization first.', 'warning')
            return redirect(url_for('auth.setup_organization'))
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# Routes
# =============================================================================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                create_audit_log(
                    action='user.login_failed',
                    details={'email': email, 'reason': 'account_inactive'},
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string[:500] if request.user_agent else None,
                    status='failure'
                )
                db.session.commit()
                return render_template('auth/login.html')

            login_user(user, remember=remember)
            user.last_login_at = datetime.utcnow()

            create_audit_log(
                action='user.login',
                user_id=user.id,
                organization_id=user.organization_id,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string[:500] if request.user_agent else None
            )
            db.session.commit()

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            create_audit_log(
                action='user.login_failed',
                details={'email': email, 'reason': 'invalid_credentials'},
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string[:500] if request.user_agent else None,
                status='failure'
            )
            db.session.commit()

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        organization_name = request.form.get('organization_name', '').strip()

        # Validation
        errors = []

        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')

        if len(password) < 8:
            errors.append('Password must be at least 8 characters.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        if not first_name or not last_name:
            errors.append('First name and last name are required.')

        if not organization_name:
            errors.append('Organization name is required.')

        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')

        # Create organization
        org_slug = re.sub(r'[^a-z0-9]+', '-', organization_name.lower()).strip('-')
        # Ensure unique slug
        base_slug = org_slug
        counter = 1
        while Organization.query.filter_by(slug=org_slug).first():
            org_slug = f"{base_slug}-{counter}"
            counter += 1

        organization = Organization(
            name=organization_name,
            slug=org_slug,
            plan='starter',
            status='active'
        )
        db.session.add(organization)
        db.session.flush()  # Get the org ID

        # Get admin role
        admin_role = Role.query.filter_by(name='admin').first()

        # Create user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            organization_id=organization.id,
            role_id=admin_role.id if admin_role else None,
            is_owner=True,
            is_active=True,
            is_verified=False  # Would need email verification in production
        )
        user.set_password(password)
        db.session.add(user)

        create_audit_log(
            action='user.register',
            user_id=user.id,
            organization_id=organization.id,
            details={'organization_name': organization_name},
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:500] if request.user_agent else None
        )

        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    create_audit_log(
        action='user.logout',
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        ip_address=request.remote_addr
    )
    db.session.commit()

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page."""
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', current_user.first_name).strip()
        current_user.last_name = request.form.get('last_name', current_user.last_name).strip()
        current_user.title = request.form.get('title', '').strip() or None
        current_user.phone = request.form.get('phone', '').strip() or None

        create_audit_log(
            action='user.profile_update',
            user_id=current_user.id,
            organization_id=current_user.organization_id,
            ip_address=request.remote_addr
        )

        db.session.commit()
        flash('Profile updated successfully.', 'success')

    return render_template('auth/profile.html', user=current_user)


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password page."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
        elif len(new_password) < 8:
            flash('New password must be at least 8 characters.', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        else:
            current_user.set_password(new_password)

            create_audit_log(
                action='user.password_change',
                user_id=current_user.id,
                organization_id=current_user.organization_id,
                ip_address=request.remote_addr
            )

            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('auth.profile'))

    return render_template('auth/change_password.html')


# =============================================================================
# Organization Management
# =============================================================================

@auth_bp.route('/organization', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.ORG_SETTINGS)
def organization_settings():
    """Organization settings page."""
    org = current_user.organization

    if request.method == 'POST':
        org.name = request.form.get('name', org.name).strip()
        org.sector = request.form.get('sector', org.sector)

        # White-label settings - colors
        primary_color = request.form.get('primary_color', '').strip()
        secondary_color = request.form.get('secondary_color', '').strip()

        if primary_color and primary_color.startswith('#'):
            org.primary_color = primary_color
        if secondary_color and secondary_color.startswith('#'):
            org.secondary_color = secondary_color

        # Handle logo file upload
        if 'logo' in request.files:
            logo_file = request.files['logo']
            if logo_file and logo_file.filename and allowed_file(logo_file.filename):
                # Generate unique filename
                ext = logo_file.filename.rsplit('.', 1)[1].lower()
                filename = f"{org.slug}-{uuid.uuid4().hex[:8]}.{ext}"
                filename = secure_filename(filename)

                # Save to uploads folder
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'logos')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                logo_file.save(filepath)

                # Update org logo URL
                org.logo_url = f"/static/uploads/logos/{filename}"

        create_audit_log(
            action='organization.settings_update',
            user_id=current_user.id,
            organization_id=org.id,
            details={'changes': 'branding_updated'},
            ip_address=request.remote_addr
        )

        db.session.commit()
        flash('Organization settings updated.', 'success')

    return render_template('auth/organization_settings.html', organization=org)


@auth_bp.route('/organization/sso', methods=['POST'])
@login_required
@permission_required(Permissions.ORG_SETTINGS)
def sso_settings():
    """Update SSO settings for the organization."""
    org = current_user.organization

    # Only enterprise plans can use SSO
    if org.plan != 'enterprise':
        flash('SSO is only available on the Enterprise plan.', 'warning')
        return redirect(url_for('auth.organization_settings'))

    # Get current settings or create new dict
    settings = org.settings or {}
    sso_config = settings.get('sso', {})

    # Update SSO settings
    sso_enabled = request.form.get('sso_enabled') == '1'
    sso_provider = request.form.get('sso_provider', '').strip()
    client_id = request.form.get('client_id', '').strip()
    client_secret = request.form.get('client_secret', '').strip()
    auto_provision = request.form.get('auto_provision') == '1'

    # Provider-specific settings
    tenant_id = request.form.get('tenant_id', '').strip()
    okta_domain = request.form.get('okta_domain', '').strip()

    # Validate required fields if SSO is enabled
    if sso_enabled:
        if not sso_provider:
            flash('Please select an identity provider.', 'danger')
            return redirect(url_for('auth.organization_settings'))
        if not client_id:
            flash('Client ID is required.', 'danger')
            return redirect(url_for('auth.organization_settings'))
        # Only require secret if not already set
        if not client_secret and not sso_config.get('client_secret'):
            flash('Client Secret is required.', 'danger')
            return redirect(url_for('auth.organization_settings'))

        # Provider-specific validation
        if sso_provider == 'azure_ad' and not tenant_id:
            flash('Azure Tenant ID is required.', 'danger')
            return redirect(url_for('auth.organization_settings'))
        if sso_provider == 'okta' and not okta_domain:
            flash('Okta Domain is required.', 'danger')
            return redirect(url_for('auth.organization_settings'))

    # Update SSO config
    sso_config['enabled'] = sso_enabled
    sso_config['provider'] = sso_provider
    sso_config['client_id'] = client_id
    sso_config['auto_provision'] = auto_provision

    # Only update secret if provided (keep existing if blank)
    if client_secret:
        sso_config['client_secret'] = client_secret

    # Provider-specific settings
    if sso_provider == 'azure_ad':
        sso_config['tenant_id'] = tenant_id
    elif sso_provider == 'okta':
        sso_config['okta_domain'] = okta_domain

    # Save settings
    settings['sso'] = sso_config
    org.settings = settings

    create_audit_log(
        action='organization.sso_settings_update',
        user_id=current_user.id,
        organization_id=org.id,
        details={'sso_enabled': sso_enabled, 'provider': sso_provider},
        ip_address=request.remote_addr
    )

    db.session.commit()
    flash('SSO settings updated successfully.', 'success')

    return redirect(url_for('auth.organization_settings'))


@auth_bp.route('/team', methods=['GET'])
@login_required
@permission_required(Permissions.USER_MANAGE)
def team_management():
    """Team management page."""
    org = current_user.organization
    users = User.query.filter_by(organization_id=org.id).all()
    roles = Role.query.all()

    return render_template('auth/team.html', users=users, roles=roles, organization=org)


@auth_bp.route('/team/invite', methods=['POST'])
@login_required
@permission_required(Permissions.USER_MANAGE)
def invite_user():
    """Invite a new user to the organization."""
    org = current_user.organization

    # Check user limit
    current_users = User.query.filter_by(organization_id=org.id).count()
    if current_users >= org.max_users:
        flash(f'User limit reached ({org.max_users}). Upgrade your plan to add more users.', 'warning')
        return redirect(url_for('auth.team_management'))

    email = request.form.get('email', '').lower().strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    role_id = request.form.get('role_id')

    if User.query.filter_by(email=email).first():
        flash('A user with this email already exists.', 'danger')
        return redirect(url_for('auth.team_management'))

    # Create user with temporary password (in production, send email invite)
    import secrets
    temp_password = secrets.token_urlsafe(12)

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        organization_id=org.id,
        role_id=role_id,
        is_active=True,
        is_verified=False
    )
    user.set_password(temp_password)
    db.session.add(user)

    create_audit_log(
        action='user.invite',
        user_id=current_user.id,
        organization_id=org.id,
        resource_type='user',
        resource_id=user.id,
        details={'invited_email': email},
        ip_address=request.remote_addr
    )

    db.session.commit()

    # In production, send email with invite link
    flash(f'User {email} invited. Temporary password: {temp_password}', 'success')
    return redirect(url_for('auth.team_management'))


@auth_bp.route('/team/<user_id>/deactivate', methods=['POST'])
@login_required
@permission_required(Permissions.USER_MANAGE)
def deactivate_user(user_id):
    """Deactivate a user."""
    user = User.query.get_or_404(user_id)

    if user.organization_id != current_user.organization_id:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.team_management'))

    if user.is_owner:
        flash('Cannot deactivate the organization owner.', 'danger')
        return redirect(url_for('auth.team_management'))

    user.is_active = not user.is_active

    create_audit_log(
        action='user.status_change',
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        resource_type='user',
        resource_id=user_id,
        details={'new_status': 'active' if user.is_active else 'inactive'},
        ip_address=request.remote_addr
    )

    db.session.commit()

    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.', 'success')
    return redirect(url_for('auth.team_management'))


# =============================================================================
# Audit Logs
# =============================================================================

@auth_bp.route('/audit-logs')
@login_required
@permission_required(Permissions.AUDIT_VIEW)
def audit_logs():
    """View audit logs."""
    page = request.args.get('page', 1, type=int)
    per_page = 50

    logs = AuditLog.query.filter_by(
        organization_id=current_user.organization_id
    ).order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('auth/audit_logs.html', logs=logs)
