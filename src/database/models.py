"""
SQLAlchemy database models for AI Practice Platform.

Provides persistent storage for assessments, leads, chat sessions, and documents.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


class Lead(db.Model):
    """Lead/contact information captured during assessment start."""

    __tablename__ = 'leads'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False, index=True)
    organization = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    sector = db.Column(db.String(50), nullable=False, default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assessments = db.relationship('Assessment', backref='lead', lazy='dynamic')

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
    sector = db.Column(db.String(50), nullable=False, default='general')
    responses = db.Column(JSON, nullable=True)  # Question responses
    result = db.Column(JSON, nullable=True)  # Scoring result
    benchmark_comparison = db.Column(JSON, nullable=True)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_sessions = db.relationship('ChatSession', backref='assessment', lazy='dynamic')
    documents = db.relationship('Document', backref='assessment', lazy='dynamic')

    # Indexes
    __table_args__ = (
        Index('idx_assessment_status_created', 'status', 'created_at'),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary."""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'sector': self.sector,
            'responses': self.responses,
            'result': self.result,
            'benchmark_comparison': self.benchmark_comparison,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


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
