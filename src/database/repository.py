"""
Repository pattern for database access.

Provides a clean interface for CRUD operations on database models.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from .models import db, Lead, Assessment, ChatSession, Document, Framework


class BaseRepository:
    """Base repository with common CRUD operations."""

    model = None

    @classmethod
    def get_by_id(cls, id: str) -> Optional[Any]:
        """Get a record by ID."""
        return cls.model.query.get(id)

    @classmethod
    def get_all(cls, limit: int = 100, offset: int = 0) -> List[Any]:
        """Get all records with pagination."""
        return cls.model.query.order_by(
            cls.model.created_at.desc()
        ).limit(limit).offset(offset).all()

    @classmethod
    def create(cls, **kwargs) -> Any:
        """Create a new record."""
        instance = cls.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def update(cls, id: str, **kwargs) -> Optional[Any]:
        """Update a record by ID."""
        instance = cls.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
        return instance

    @classmethod
    def delete(cls, id: str) -> bool:
        """Delete a record by ID."""
        instance = cls.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False

    @classmethod
    def count(cls) -> int:
        """Get total count of records."""
        return cls.model.query.count()


class LeadRepository(BaseRepository):
    """Repository for Lead model."""

    model = Lead

    @classmethod
    def get_by_email(cls, email: str) -> Optional[Lead]:
        """Get a lead by email address."""
        return Lead.query.filter_by(email=email.lower()).first()

    @classmethod
    def get_by_organization(cls, organization: str) -> List[Lead]:
        """Get all leads from an organization."""
        return Lead.query.filter_by(organization=organization).all()

    @classmethod
    def search(cls, query: str, limit: int = 20) -> List[Lead]:
        """Search leads by name, email, or organization."""
        search_term = f"%{query}%"
        return Lead.query.filter(
            db.or_(
                Lead.name.ilike(search_term),
                Lead.email.ilike(search_term),
                Lead.organization.ilike(search_term)
            )
        ).limit(limit).all()


class AssessmentRepository(BaseRepository):
    """Repository for Assessment model."""

    model = Assessment

    @classmethod
    def get_by_lead(cls, lead_id: str) -> List[Assessment]:
        """Get all assessments for a lead."""
        return Assessment.query.filter_by(lead_id=lead_id).order_by(
            Assessment.created_at.desc()
        ).all()

    @classmethod
    def get_completed(cls, limit: int = 100) -> List[Assessment]:
        """Get completed assessments."""
        return Assessment.query.filter_by(status='completed').order_by(
            Assessment.completed_at.desc()
        ).limit(limit).all()

    @classmethod
    def get_in_progress(cls) -> List[Assessment]:
        """Get in-progress assessments."""
        return Assessment.query.filter_by(status='in_progress').all()

    @classmethod
    def complete(cls, id: str, result: Dict, benchmark_comparison: Dict = None) -> Optional[Assessment]:
        """Mark an assessment as completed with results."""
        assessment = cls.get_by_id(id)
        if assessment:
            assessment.result = result
            assessment.benchmark_comparison = benchmark_comparison
            assessment.status = 'completed'
            assessment.completed_at = datetime.utcnow()
            db.session.commit()
        return assessment

    @classmethod
    def update_responses(cls, id: str, responses: Dict) -> Optional[Assessment]:
        """Update assessment responses."""
        assessment = cls.get_by_id(id)
        if assessment:
            if assessment.responses is None:
                assessment.responses = {}
            assessment.responses.update(responses)
            db.session.commit()
        return assessment

    @classmethod
    def get_by_sector(cls, sector: str, limit: int = 100) -> List[Assessment]:
        """Get assessments by sector."""
        return Assessment.query.filter_by(
            sector=sector, status='completed'
        ).order_by(Assessment.created_at.desc()).limit(limit).all()

    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Get assessment statistics."""
        total = cls.count()
        completed = Assessment.query.filter_by(status='completed').count()
        in_progress = Assessment.query.filter_by(status='in_progress').count()

        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }


class ChatSessionRepository(BaseRepository):
    """Repository for ChatSession model."""

    model = ChatSession

    @classmethod
    def get_by_assessment(cls, assessment_id: str) -> List[ChatSession]:
        """Get all chat sessions for an assessment."""
        return ChatSession.query.filter_by(
            assessment_id=assessment_id
        ).order_by(ChatSession.created_at.desc()).all()

    @classmethod
    def get_active(cls) -> List[ChatSession]:
        """Get all active chat sessions."""
        return ChatSession.query.filter_by(is_active=True).all()

    @classmethod
    def deactivate(cls, id: str) -> Optional[ChatSession]:
        """Deactivate a chat session."""
        session = cls.get_by_id(id)
        if session:
            session.is_active = False
            db.session.commit()
        return session

    @classmethod
    def add_message(cls, id: str, role: str, content: str) -> Optional[ChatSession]:
        """Add a message to a chat session."""
        session = cls.get_by_id(id)
        if session:
            if session.messages is None:
                session.messages = []
            session.messages = session.messages + [{
                'role': role,
                'content': content,
                'timestamp': datetime.utcnow().isoformat()
            }]
            db.session.commit()
        return session

    @classmethod
    def get_messages(cls, id: str) -> List[Dict]:
        """Get all messages from a chat session."""
        session = cls.get_by_id(id)
        return session.messages if session and session.messages else []


class DocumentRepository(BaseRepository):
    """Repository for Document model."""

    model = Document

    @classmethod
    def get_by_assessment(cls, assessment_id: str) -> List[Document]:
        """Get all documents for an assessment."""
        return Document.query.filter_by(
            assessment_id=assessment_id
        ).order_by(Document.created_at.desc()).all()

    @classmethod
    def get_by_type(cls, doc_type: str, limit: int = 50) -> List[Document]:
        """Get documents by type."""
        return Document.query.filter_by(
            doc_type=doc_type
        ).order_by(Document.created_at.desc()).limit(limit).all()

    @classmethod
    def get_recent(cls, limit: int = 10) -> List[Document]:
        """Get recently generated documents."""
        return Document.query.order_by(
            Document.created_at.desc()
        ).limit(limit).all()


class FrameworkRepository(BaseRepository):
    """Repository for Framework model."""

    model = Framework

    @classmethod
    def get_by_assessment(cls, assessment_id: str) -> List[Framework]:
        """Get all frameworks for an assessment."""
        return Framework.query.filter_by(
            assessment_id=assessment_id
        ).order_by(Framework.created_at.desc()).all()

    @classmethod
    def get_by_type(cls, framework_type: str, limit: int = 50) -> List[Framework]:
        """Get frameworks by type."""
        return Framework.query.filter_by(
            framework_type=framework_type
        ).order_by(Framework.created_at.desc()).limit(limit).all()

    @classmethod
    def get_latest_for_assessment(cls, assessment_id: str, framework_type: str) -> Optional[Framework]:
        """Get the latest framework of a type for an assessment."""
        return Framework.query.filter_by(
            assessment_id=assessment_id,
            framework_type=framework_type
        ).order_by(Framework.created_at.desc()).first()
