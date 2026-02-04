"""
SSO Authentication Blueprint for AI Practice Platform.

Provides optional Single Sign-On (SSO) via Azure AD and Okta.
This is an OPTIONAL addition - standard username/password auth remains available.
"""

import os
import secrets
from flask import Blueprint, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, current_user
from authlib.integrations.flask_client import OAuth

from database import db, User, Organization

sso_bp = Blueprint('sso', __name__, url_prefix='/sso')

# OAuth instance (initialized lazily)
oauth = OAuth()


def init_sso(app):
    """Initialize SSO with the Flask app."""
    oauth.init_app(app)


def get_sso_config(org):
    """Get SSO configuration for an organization."""
    if not org or not org.settings:
        return None

    sso_settings = org.settings.get('sso', {})
    if not sso_settings.get('enabled'):
        return None

    return sso_settings


def is_sso_enabled(org):
    """Check if SSO is enabled for an organization."""
    config = get_sso_config(org)
    return config is not None and config.get('enabled', False)


def register_oauth_client(org):
    """
    Dynamically register OAuth client for an organization.
    Supports Azure AD and Okta.
    """
    config = get_sso_config(org)
    if not config:
        return None

    provider = config.get('provider', '').lower()
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')

    if not client_id or not client_secret:
        return None

    client_name = f"sso_{org.slug}"

    # Check if already registered
    if client_name in oauth._registry:
        return oauth._registry[client_name]

    if provider == 'azure_ad' or provider == 'azure':
        tenant_id = config.get('tenant_id', 'common')
        oauth.register(
            name=client_name,
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f'https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
    elif provider == 'okta':
        okta_domain = config.get('okta_domain')  # e.g., 'dev-123456.okta.com'
        if not okta_domain:
            return None
        oauth.register(
            name=client_name,
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url=f'https://{okta_domain}/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
    elif provider == 'google':
        oauth.register(
            name=client_name,
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
    else:
        return None

    return oauth._registry.get(client_name)


# =============================================================================
# SSO Routes
# =============================================================================

@sso_bp.route('/login/<org_slug>')
def sso_login(org_slug):
    """Initiate SSO login for an organization."""
    org = Organization.query.filter_by(slug=org_slug, status='active').first()
    if not org:
        flash('Organization not found.', 'danger')
        return redirect(url_for('index'))

    if not is_sso_enabled(org):
        flash('SSO is not enabled for this organization.', 'warning')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))

    # Register OAuth client
    client = register_oauth_client(org)
    if not client:
        flash('SSO configuration error. Please contact support.', 'danger')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))

    # Store org_slug in session for callback
    session['sso_org_slug'] = org_slug

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['sso_state'] = state

    # Redirect to IdP
    redirect_uri = url_for('sso.sso_callback', org_slug=org_slug, _external=True)
    return client.authorize_redirect(redirect_uri, state=state)


@sso_bp.route('/callback/<org_slug>')
def sso_callback(org_slug):
    """Handle SSO callback from identity provider."""
    org = Organization.query.filter_by(slug=org_slug, status='active').first()
    if not org:
        flash('Organization not found.', 'danger')
        return redirect(url_for('index'))

    if not is_sso_enabled(org):
        flash('SSO is not enabled for this organization.', 'warning')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))

    # Verify state
    stored_state = session.pop('sso_state', None)
    received_state = request.args.get('state')
    if not stored_state or stored_state != received_state:
        flash('Invalid SSO state. Please try again.', 'danger')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))

    # Get OAuth client
    client = register_oauth_client(org)
    if not client:
        flash('SSO configuration error.', 'danger')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))

    try:
        # Exchange code for token
        token = client.authorize_access_token()

        # Get user info
        userinfo = token.get('userinfo')
        if not userinfo:
            userinfo = client.userinfo()

        email = userinfo.get('email', '').lower()
        if not email:
            flash('Could not get email from SSO provider.', 'danger')
            return redirect(url_for('portal.portal_login', org_slug=org_slug))

        # Find or create user
        user = User.query.filter_by(email=email).first()

        if user:
            # User exists - verify they belong to this organization
            if user.organization_id != org.id:
                flash('Your account is not associated with this organization.', 'danger')
                return redirect(url_for('portal.portal_login', org_slug=org_slug))

            if not user.is_active:
                flash('Your account has been deactivated.', 'danger')
                return redirect(url_for('portal.portal_login', org_slug=org_slug))
        else:
            # Check if auto-provisioning is enabled
            sso_config = get_sso_config(org)
            if not sso_config.get('auto_provision', False):
                flash('Your account does not exist. Please contact your administrator.', 'warning')
                return redirect(url_for('portal.portal_login', org_slug=org_slug))

            # Auto-provision new user
            first_name = userinfo.get('given_name') or userinfo.get('name', '').split()[0] or 'User'
            last_name = userinfo.get('family_name') or (userinfo.get('name', '').split()[1:] or [''])[0]

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                organization_id=org.id,
                is_active=True,
                sso_provider=sso_config.get('provider', 'sso')
            )
            # Set a random password (user will use SSO to login)
            user.set_password(secrets.token_urlsafe(32))
            db.session.add(user)
            db.session.commit()

        # Log the user in
        login_user(user, remember=True)

        # Set session variables
        session['organization_id'] = org.id
        session['organization'] = org.name
        session['portal_slug'] = org_slug
        session['sso_login'] = True

        flash(f'Welcome, {user.first_name}!', 'success')
        return redirect(url_for('portal.portal_dashboard', org_slug=org_slug))

    except Exception as e:
        current_app.logger.error(f"SSO callback error: {e}")
        flash('SSO authentication failed. Please try again or use password login.', 'danger')
        return redirect(url_for('portal.portal_login', org_slug=org_slug))


@sso_bp.route('/logout/<org_slug>')
def sso_logout(org_slug):
    """Handle SSO logout (redirect to portal logout)."""
    # The actual logout is handled by the portal blueprint
    # This route can be extended for IdP-initiated logout if needed
    return redirect(url_for('portal.portal_logout', org_slug=org_slug))
