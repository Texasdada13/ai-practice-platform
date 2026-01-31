"""
AI Chat Engine

Sophisticated conversational AI for consulting interactions.
Manages conversation state, context injection, and response enhancement.
"""

import uuid
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .claude_client import ClaudeClient, get_claude_client

logger = logging.getLogger(__name__)


class ConversationMode(Enum):
    """Chat conversation modes"""
    GENERAL = "general"
    ASSESSMENT_GUIDE = "assessment_guide"
    RESULTS_DISCUSSION = "results_discussion"
    ROADMAP_PLANNING = "roadmap_planning"
    FRAMEWORK_BUILDER = "framework_builder"
    USE_CASE_DISCOVERY = "use_case_discovery"


@dataclass
class ChatSession:
    """Active chat session with context"""
    session_id: str
    organization_name: str
    mode: ConversationMode = ConversationMode.GENERAL
    assessment_result: Optional[Dict] = None
    sector: str = "general"
    conversation_history: List[Dict] = field(default_factory=list)
    context_data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)


class AIChatEngine:
    """
    AI-powered chat engine for consulting interactions.

    Features:
    - Context-aware responses based on assessment results
    - Multiple conversation modes
    - Suggested questions and prompts
    - Session management
    """

    # Suggested prompts by mode
    SUGGESTED_PROMPTS = {
        ConversationMode.GENERAL: [
            "What are the key steps to starting an AI initiative?",
            "How do we build executive support for AI?",
            "What common mistakes should we avoid in AI adoption?",
            "How do we measure AI ROI?"
        ],
        ConversationMode.ASSESSMENT_GUIDE: [
            "Help me understand this question better",
            "What's the difference between these options?",
            "How should I rate our organization?",
            "Can you give me examples of each maturity level?"
        ],
        ConversationMode.RESULTS_DISCUSSION: [
            "Explain our biggest gaps and how to address them",
            "What should be our top 3 priorities?",
            "How do we compare to industry benchmarks?",
            "What quick wins can we pursue immediately?"
        ],
        ConversationMode.ROADMAP_PLANNING: [
            "Create a 12-month AI roadmap for us",
            "What resources do we need for Phase 1?",
            "How should we structure our AI team?",
            "What milestones should we target?"
        ],
        ConversationMode.FRAMEWORK_BUILDER: [
            "Help me build an AI governance framework",
            "What should our AI ethics policy include?",
            "Create a data governance framework for AI",
            "Design an AI use case prioritization matrix"
        ],
        ConversationMode.USE_CASE_DISCOVERY: [
            "Identify AI use cases for our industry",
            "How do we prioritize AI opportunities?",
            "What data do we need for these use cases?",
            "Estimate ROI for the top use cases"
        ]
    }

    # Mode-specific system context additions
    MODE_CONTEXTS = {
        ConversationMode.ASSESSMENT_GUIDE: """
You are currently helping the user complete their AI readiness assessment.
Guide them through the questions, explain concepts, and help them accurately
rate their organization's capabilities.""",

        ConversationMode.RESULTS_DISCUSSION: """
You are discussing the user's AI readiness assessment results.
Help them understand their scores, identify key gaps, and prioritize next steps.
Be specific about what each score means and how to improve.""",

        ConversationMode.ROADMAP_PLANNING: """
You are helping create an AI implementation roadmap.
Consider their current maturity level, resources, and goals.
Provide realistic timelines and clear milestones.""",

        ConversationMode.FRAMEWORK_BUILDER: """
You are helping build AI frameworks and policies.
Create comprehensive, practical documents they can implement.
Include specific examples and templates where helpful.""",

        ConversationMode.USE_CASE_DISCOVERY: """
You are facilitating AI use case discovery and prioritization.
Help identify high-value opportunities based on their industry and capabilities.
Consider feasibility, impact, and data requirements."""
    }

    def __init__(self, claude_client: Optional[ClaudeClient] = None):
        """Initialize chat engine"""
        self.claude = claude_client or get_claude_client()
        self.sessions: Dict[str, ChatSession] = {}

    def create_session(
        self,
        organization_name: str,
        sector: str = "general",
        assessment_result: Optional[Dict] = None,
        mode: ConversationMode = ConversationMode.GENERAL
    ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            organization_name: Name of the organization
            sector: Industry sector
            assessment_result: Optional assessment results for context
            mode: Initial conversation mode

        Returns:
            New ChatSession
        """
        session_id = str(uuid.uuid4())

        session = ChatSession(
            session_id=session_id,
            organization_name=organization_name,
            mode=mode,
            assessment_result=assessment_result,
            sector=sector
        )

        # Build context for Claude
        context = self._build_context(session)
        self.claude.create_conversation(session_id, "consultant", context)

        self.sessions[session_id] = session
        logger.info(f"Created chat session {session_id} for {organization_name}")

        return session

    def _build_context(self, session: ChatSession) -> Dict[str, Any]:
        """Build context dictionary for Claude"""
        context = {
            "organization_name": session.organization_name,
            "sector": session.sector,
            "conversation_mode": session.mode.value
        }

        if session.assessment_result:
            context["assessment_result"] = {
                "overall_score": session.assessment_result.get("overall_score"),
                "maturity_level": session.assessment_result.get("maturity_level"),
                "grade": session.assessment_result.get("grade"),
                "dimension_scores": session.assessment_result.get("dimension_scores"),
                "top_strengths": session.assessment_result.get("top_strengths"),
                "top_improvements": session.assessment_result.get("top_improvements"),
                "recommendations": session.assessment_result.get("recommendations")
            }

        # Add mode-specific context
        if session.mode in self.MODE_CONTEXTS:
            context["mode_instructions"] = self.MODE_CONTEXTS[session.mode]

        return context

    def chat(
        self,
        session_id: str,
        user_message: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Process a chat message.

        Args:
            session_id: Session ID
            user_message: User's message
            stream: Whether to stream response

        Returns:
            Response with message and metadata
        """
        if session_id not in self.sessions:
            return {
                "error": "Session not found",
                "message": "Please start a new conversation."
            }

        session = self.sessions[session_id]
        session.last_activity = datetime.now()

        # Add to conversation history
        session.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })

        # Get response from Claude
        response = self.claude.chat(session_id, user_message, stream=stream)

        # Add assistant response to history
        session.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "message": response,
            "session_id": session_id,
            "mode": session.mode.value,
            "suggested_prompts": self.get_suggested_prompts(session_id),
            "timestamp": datetime.now().isoformat()
        }

    def change_mode(self, session_id: str, new_mode: ConversationMode) -> bool:
        """Change conversation mode for a session"""
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        session.mode = new_mode

        # Update Claude context
        context = self._build_context(session)
        self.claude.create_conversation(session_id, "consultant", context)

        # Preserve conversation history
        for msg in session.conversation_history:
            self.claude.conversations[session_id].add_message(
                msg["role"], msg["content"]
            )

        logger.info(f"Changed session {session_id} to mode {new_mode.value}")
        return True

    def get_suggested_prompts(self, session_id: str) -> List[str]:
        """Get suggested prompts based on current mode"""
        if session_id not in self.sessions:
            return self.SUGGESTED_PROMPTS[ConversationMode.GENERAL]

        session = self.sessions[session_id]
        base_prompts = self.SUGGESTED_PROMPTS.get(
            session.mode,
            self.SUGGESTED_PROMPTS[ConversationMode.GENERAL]
        )

        # Add context-aware prompts if we have assessment results
        if session.assessment_result and session.mode == ConversationMode.RESULTS_DISCUSSION:
            score = session.assessment_result.get("overall_score", 50)
            if score < 40:
                base_prompts = [
                    "What foundational capabilities should we build first?",
                    "How do we get executive buy-in for AI investment?",
                ] + base_prompts[:2]
            elif score >= 70:
                base_prompts = [
                    "How do we scale our AI initiatives across the enterprise?",
                    "What advanced AI capabilities should we explore?",
                ] + base_prompts[:2]

        return base_prompts

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def update_assessment_result(self, session_id: str, result: Dict) -> bool:
        """Update assessment result for a session"""
        if session_id not in self.sessions:
            return False

        session = self.sessions[session_id]
        session.assessment_result = result

        # Rebuild context
        context = self._build_context(session)
        self.claude.conversations[session_id].context = context

        return True

    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of conversation"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]

        return {
            "session_id": session_id,
            "organization_name": session.organization_name,
            "sector": session.sector,
            "mode": session.mode.value,
            "message_count": len(session.conversation_history),
            "has_assessment": session.assessment_result is not None,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat()
        }

    def export_conversation(self, session_id: str) -> Dict[str, Any]:
        """Export full conversation for saving/reporting"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]

        return {
            "session_id": session_id,
            "organization_name": session.organization_name,
            "sector": session.sector,
            "assessment_score": session.assessment_result.get("overall_score") if session.assessment_result else None,
            "conversation": session.conversation_history,
            "exported_at": datetime.now().isoformat()
        }


# Singleton instance
_engine: Optional[AIChatEngine] = None


def get_chat_engine() -> AIChatEngine:
    """Get or create singleton chat engine"""
    global _engine
    if _engine is None:
        _engine = AIChatEngine()
    return _engine
