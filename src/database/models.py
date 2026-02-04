"""
SQLAlchemy database models for AI Practice Platform.

Provides persistent storage for assessments, leads, chat sessions, documents,
and enterprise features (users, organizations, audit logs).
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event
from sqlalchemy.dialects.sqlite import JSON
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


# =============================================================================
# ENTERPRISE MODELS - Organizations, Users, Roles
# =============================================================================

class Organization(db.Model):
    """Organization/tenant for multi-client support."""

    __tablename__ = 'organizations'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    sector = db.Column(db.String(50), default='general')

    # Subscription & Status
    plan = db.Column(db.String(50), default='starter')  # starter, professional, enterprise
    status = db.Column(db.String(20), default='active')  # active, suspended, cancelled
    max_users = db.Column(db.Integer, default=3)
    max_assessments_per_month = db.Column(db.Integer, default=5)

    # White-label branding
    logo_url = db.Column(db.String(500), nullable=True)
    primary_color = db.Column(db.String(7), default='#1a365d')  # Hex color
    secondary_color = db.Column(db.String(7), default='#2b6cb0')
    custom_domain = db.Column(db.String(255), nullable=True)

    # Settings
    settings = db.Column(JSON, default=dict)  # Additional org settings

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    assessments = db.relationship('Assessment', backref='organization', lazy='dynamic')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'sector': self.sector,
            'plan': self.plan,
            'status': self.status,
            'max_users': self.max_users,
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def get_branding(self) -> Dict[str, Any]:
        """Get branding settings for white-label."""
        return {
            'logo_url': self.logo_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'name': self.name
        }


class Role(db.Model):
    """User roles for RBAC."""

    __tablename__ = 'roles'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    permissions = db.Column(JSON, default=list)  # List of permission strings

    # Default roles: admin, analyst, viewer

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions
        }

    def has_permission(self, permission: str) -> bool:
        return permission in (self.permissions or [])


class User(db.Model):
    """User accounts with authentication."""

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)

    # Organization & Role
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True, index=True)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=True)
    role = db.relationship('Role', backref='users')

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)  # Organization owner

    # SSO
    sso_provider = db.Column(db.String(50), nullable=True)  # azure_ad, okta, google, etc.

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    assessments = db.relationship('Assessment', backref='created_by_user', lazy='dynamic',
                                  foreign_keys='Assessment.created_by')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password: str):
        """Hash and set the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        if self.is_owner:
            return True  # Owners have all permissions
        if self.role:
            return self.role.has_permission(permission)
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'title': self.title,
            'organization_id': self.organization_id,
            'role': self.role.name if self.role else None,
            'is_active': self.is_active,
            'is_owner': self.is_owner,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }


class AuditLog(db.Model):
    """Audit log for tracking all user actions."""

    __tablename__ = 'audit_logs'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True, index=True)

    # Action details
    action = db.Column(db.String(100), nullable=False)  # e.g., 'assessment.create', 'user.login'
    resource_type = db.Column(db.String(50), nullable=True)  # e.g., 'assessment', 'document'
    resource_id = db.Column(db.String(36), nullable=True)

    # Request context
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)

    # Additional data
    details = db.Column(JSON, nullable=True)  # Any extra context
    status = db.Column(db.String(20), default='success')  # success, failure

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_audit_action_created', 'action', 'created_at'),
        Index('idx_audit_org_created', 'organization_id', 'created_at'),
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'details': self.details,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AssessmentVersion(db.Model):
    """Track assessment versions over time for progress tracking."""

    __tablename__ = 'assessment_versions'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=False, index=True)
    version_number = db.Column(db.Integer, nullable=False)

    # Snapshot of assessment at this version
    responses = db.Column(JSON, nullable=True)
    result = db.Column(JSON, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)

    # Metadata
    notes = db.Column(db.Text, nullable=True)  # Optional notes about this version
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_version_assessment_number', 'assessment_id', 'version_number'),
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'version_number': self.version_number,
            'overall_score': self.overall_score,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# =============================================================================
# PERMISSIONS CONSTANTS
# =============================================================================

class Permissions:
    """Permission constants for RBAC."""

    # Assessment permissions
    ASSESSMENT_VIEW = 'assessment.view'
    ASSESSMENT_CREATE = 'assessment.create'
    ASSESSMENT_EDIT = 'assessment.edit'
    ASSESSMENT_DELETE = 'assessment.delete'

    # Framework permissions
    FRAMEWORK_VIEW = 'framework.view'
    FRAMEWORK_CREATE = 'framework.create'

    # Document permissions
    DOCUMENT_VIEW = 'document.view'
    DOCUMENT_CREATE = 'document.create'
    DOCUMENT_EXPORT = 'document.export'

    # Chat permissions
    CHAT_ACCESS = 'chat.access'

    # Admin permissions
    USER_MANAGE = 'user.manage'
    ORG_SETTINGS = 'org.settings'
    BILLING_MANAGE = 'billing.manage'
    AUDIT_VIEW = 'audit.view'

    @classmethod
    def admin_permissions(cls) -> List[str]:
        """All permissions for admin role."""
        return [
            cls.ASSESSMENT_VIEW, cls.ASSESSMENT_CREATE, cls.ASSESSMENT_EDIT, cls.ASSESSMENT_DELETE,
            cls.FRAMEWORK_VIEW, cls.FRAMEWORK_CREATE,
            cls.DOCUMENT_VIEW, cls.DOCUMENT_CREATE, cls.DOCUMENT_EXPORT,
            cls.CHAT_ACCESS,
            cls.USER_MANAGE, cls.ORG_SETTINGS, cls.AUDIT_VIEW
        ]

    @classmethod
    def analyst_permissions(cls) -> List[str]:
        """Permissions for analyst role."""
        return [
            cls.ASSESSMENT_VIEW, cls.ASSESSMENT_CREATE, cls.ASSESSMENT_EDIT,
            cls.FRAMEWORK_VIEW, cls.FRAMEWORK_CREATE,
            cls.DOCUMENT_VIEW, cls.DOCUMENT_CREATE, cls.DOCUMENT_EXPORT,
            cls.CHAT_ACCESS
        ]

    @classmethod
    def viewer_permissions(cls) -> List[str]:
        """Permissions for viewer role."""
        return [
            cls.ASSESSMENT_VIEW,
            cls.FRAMEWORK_VIEW,
            cls.DOCUMENT_VIEW,
            cls.CHAT_ACCESS
        ]


# =============================================================================
# ORIGINAL MODELS (updated with organization support)
# =============================================================================


class Lead(db.Model):
    """Lead/contact information captured during assessment start."""

    __tablename__ = 'leads'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False, index=True)
    organization_name = db.Column(db.String(200), nullable=False)  # Renamed for clarity
    title = db.Column(db.String(100), nullable=True)
    sector = db.Column(db.String(50), nullable=False, default='general')
    phone = db.Column(db.String(20), nullable=True)
    source = db.Column(db.String(50), nullable=True)  # How they found us

    # Link to organization (if converted to customer)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True, index=True)
    converted_to_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assessments = db.relationship('Assessment', backref='lead', lazy='dynamic')

    # Backwards compatibility property
    @property
    def organization(self):
        return self.organization_name

    @organization.setter
    def organization(self, value):
        self.organization_name = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert lead to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'organization': self.organization,
            'title': self.title,
            'sector': self.sector,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Assessment(db.Model):
    """Assessment data including responses and results."""

    __tablename__ = 'assessments'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=True, index=True)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True, index=True)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)

    # Assessment details
    name = db.Column(db.String(200), nullable=True)  # Optional assessment name
    sector = db.Column(db.String(50), nullable=False, default='general')
    responses = db.Column(JSON, nullable=True)  # Question responses
    result = db.Column(JSON, nullable=True)  # Scoring result
    benchmark_comparison = db.Column(JSON, nullable=True)

    # Status tracking
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, archived
    current_version = db.Column(db.Integer, default=1)
    is_demo = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='assessment', lazy='dynamic')
    documents = db.relationship('Document', backref='assessment', lazy='dynamic')
    versions = db.relationship('AssessmentVersion', backref='assessment', lazy='dynamic',
                               order_by='AssessmentVersion.version_number.desc()')

    # Indexes
    __table_args__ = (
        Index('idx_assessment_status_created', 'status', 'created_at'),
        Index('idx_assessment_org_status', 'organization_id', 'status'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary."""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'organization_id': self.organization_id,
            'created_by': self.created_by,
            'name': self.name,
            'sector': self.sector,
            'responses': self.responses,
            'result': self.result,
            'benchmark_comparison': self.benchmark_comparison,
            'status': self.status,
            'current_version': self.current_version,
            'is_demo': self.is_demo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def create_version(self, notes: str = None, user_id: str = None) -> 'AssessmentVersion':
        """Create a new version snapshot of this assessment."""
        version = AssessmentVersion(
            assessment_id=self.id,
            version_number=self.current_version,
            responses=self.responses,
            result=self.result,
            overall_score=self.result.get('overall_score') if self.result else None,
            notes=notes,
            created_by=user_id
        )
        self.current_version += 1
        return version


class ChatSession(db.Model):
    """Chat session data for AI consultant conversations."""

    __tablename__ = 'chat_sessions'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=True, index=True)
    organization = db.Column(db.String(200), nullable=True)
    sector = db.Column(db.String(50), nullable=True)
    mode = db.Column(db.String(50), default='general')
    messages = db.Column(JSON, default=list)  # Chat history
    context = db.Column(JSON, nullable=True)  # Additional context
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert chat session to dictionary."""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'organization': self.organization,
            'sector': self.sector,
            'mode': self.mode,
            'message_count': len(self.messages) if self.messages else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        if self.messages is None:
            self.messages = []
        self.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        })


class Document(db.Model):
    """Generated document storage."""

    __tablename__ = 'documents'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=True, index=True)
    doc_type = db.Column(db.String(50), nullable=False)  # executive_summary, strategy, etc.
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)  # Markdown content
    sections = db.Column(JSON, nullable=True)  # Structured sections
    format = db.Column(db.String(20), default='markdown')  # markdown, pdf, docx
    word_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(500), nullable=True)  # Path to generated file
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    organization = db.Column(db.String(200), nullable=True)
    sector = db.Column(db.String(50), nullable=True)

    # Indexes
    __table_args__ = (
        Index('idx_document_type_created', 'doc_type', 'created_at'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'doc_type': self.doc_type,
            'title': self.title,
            'word_count': self.word_count,
            'format': self.format,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'organization': self.organization,
            'sector': self.sector
        }


class Framework(db.Model):
    """Generated framework storage."""

    __tablename__ = 'frameworks'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assessment_id = db.Column(db.String(36), db.ForeignKey('assessments.id'), nullable=True, index=True)
    framework_type = db.Column(db.String(50), nullable=False)  # strategy, governance, ethics, mlops, data
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(JSON, nullable=True)  # Framework data
    organization = db.Column(db.String(200), nullable=True)
    sector = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert framework to dictionary."""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'framework_type': self.framework_type,
            'title': self.title,
            'organization': self.organization,
            'sector': self.sector,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        _create_default_roles()


def _create_default_roles():
    """Create default roles if they don't exist."""
    default_roles = [
        {
            'name': 'admin',
            'description': 'Full access to all features and settings',
            'permissions': Permissions.admin_permissions()
        },
        {
            'name': 'analyst',
            'description': 'Can create and manage assessments and documents',
            'permissions': Permissions.analyst_permissions()
        },
        {
            'name': 'viewer',
            'description': 'Read-only access to assessments and documents',
            'permissions': Permissions.viewer_permissions()
        }
    ]

    for role_data in default_roles:
        existing = Role.query.filter_by(name=role_data['name']).first()
        if not existing:
            role = Role(
                name=role_data['name'],
                description=role_data['description'],
                permissions=role_data['permissions']
            )
            db.session.add(role)

    db.session.commit()


def create_audit_log(
    action: str,
    user_id: str = None,
    organization_id: str = None,
    resource_type: str = None,
    resource_id: str = None,
    details: Dict = None,
    ip_address: str = None,
    user_agent: str = None,
    status: str = 'success'
) -> AuditLog:
    """Helper function to create audit log entries."""
    log = AuditLog(
        action=action,
        user_id=user_id,
        organization_id=organization_id,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status
    )
    db.session.add(log)
    return log
