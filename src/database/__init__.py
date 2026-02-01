"""
Database module for AI Practice Platform.

Provides SQLAlchemy models and database utilities.
"""

from .models import (
    db, init_db, generate_uuid, create_audit_log,
    # Core models
    Lead, Assessment, ChatSession, Document, Framework,
    # Enterprise models
    Organization, User, Role, AuditLog, AssessmentVersion,
    # Permissions
    Permissions
)
from .repository import (
    LeadRepository,
    AssessmentRepository,
    ChatSessionRepository,
    DocumentRepository
)

__all__ = [
    # Database
    'db',
    'init_db',
    'generate_uuid',
    'create_audit_log',
    # Core models
    'Lead',
    'Assessment',
    'ChatSession',
    'Document',
    'Framework',
    # Enterprise models
    'Organization',
    'User',
    'Role',
    'AuditLog',
    'AssessmentVersion',
    'Permissions',
    # Repositories
    'LeadRepository',
    'AssessmentRepository',
    'ChatSessionRepository',
    'DocumentRepository'
]
