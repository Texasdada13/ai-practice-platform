"""
Database module for AI Practice Platform.

Provides SQLAlchemy models and database utilities.
"""

from .models import db, Lead, Assessment, ChatSession, Document, init_db
from .repository import (
    LeadRepository,
    AssessmentRepository,
    ChatSessionRepository,
    DocumentRepository
)

__all__ = [
    'db',
    'init_db',
    'Lead',
    'Assessment',
    'ChatSession',
    'Document',
    'LeadRepository',
    'AssessmentRepository',
    'ChatSessionRepository',
    'DocumentRepository'
]
