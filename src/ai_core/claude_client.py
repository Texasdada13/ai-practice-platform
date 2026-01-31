"""
Claude API Client

Wrapper for Anthropic's Claude API providing:
- Conversation management
- Context injection
- Streaming responses
- Error handling and retries
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Generator
from dataclasses import dataclass, field
from datetime import datetime

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Chat message"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    """Conversation context"""
    id: str
    messages: List[Message] = field(default_factory=list)
    system_prompt: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def add_message(self, role: str, content: str, **metadata) -> Message:
        msg = Message(role=role, content=content, metadata=metadata)
        self.messages.append(msg)
        return msg

    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Format messages for Claude API"""
        return [{"role": m.role, "content": m.content} for m in self.messages]


class ClaudeClient:
    """
    Claude API Client for AI Practice Platform.

    Provides high-level interface for:
    - AI consulting conversations
    - Document generation
    - Assessment analysis
    - Recommendation generation
    """

    DEFAULT_MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 4096

    # System prompts for different contexts
    SYSTEM_PROMPTS = {
        "consultant": """You are an expert AI Strategy Consultant helping organizations assess their AI readiness and build AI capabilities. You work for Patriot Tech Systems Consulting.

Your expertise includes:
- AI/ML strategy and roadmaps
- Data maturity assessment
- Technology infrastructure evaluation
- AI governance and ethics
- Change management for AI adoption
- Use case identification and prioritization

When advising clients:
1. Be specific and actionable - provide concrete next steps
2. Reference industry best practices and frameworks
3. Consider their current maturity level
4. Balance ambition with pragmatism
5. Highlight risks and how to mitigate them

You have access to their assessment results which will be provided in the context.""",

        "document_writer": """You are a professional business document writer specializing in AI strategy and transformation documents. Create clear, executive-ready content.

Document style guidelines:
- Use professional business language
- Include specific metrics and targets where appropriate
- Structure content with clear headers and sections
- Provide actionable recommendations
- Balance strategic vision with tactical details""",

        "analyst": """You are a data analyst specializing in AI readiness assessment. Analyze the provided assessment data and provide insights.

Focus on:
- Identifying patterns and correlations
- Highlighting strengths and gaps
- Comparing to industry benchmarks
- Prioritizing areas for improvement
- Quantifying potential impact"""
    }

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (defaults to claude-sonnet-4-20250514)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = model or self.DEFAULT_MODEL
        self.client = None
        self.conversations: Dict[str, Conversation] = {}

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            logger.info(f"Claude client initialized with model {self.model}")
        else:
            logger.warning("Anthropic SDK not available or no API key - using fallback mode")

    def is_available(self) -> bool:
        """Check if Claude API is available"""
        return self.client is not None

    def create_conversation(
        self,
        conversation_id: str,
        context_type: str = "consultant",
        custom_context: Optional[Dict[str, Any]] = None
    ) -> Conversation:
        """
        Create a new conversation with context.

        Args:
            conversation_id: Unique ID for this conversation
            context_type: Type of system prompt to use
            custom_context: Additional context data

        Returns:
            Conversation object
        """
        system_prompt = self.SYSTEM_PROMPTS.get(context_type, self.SYSTEM_PROMPTS["consultant"])

        # Add custom context to system prompt if provided
        if custom_context:
            context_str = "\n\nCONTEXT DATA:\n" + json.dumps(custom_context, indent=2, default=str)
            system_prompt += context_str

        conversation = Conversation(
            id=conversation_id,
            system_prompt=system_prompt,
            context=custom_context or {}
        )
        self.conversations[conversation_id] = conversation
        return conversation

    def chat(
        self,
        conversation_id: str,
        user_message: str,
        stream: bool = False
    ) -> str:
        """
        Send a message and get response.

        Args:
            conversation_id: Conversation to continue
            user_message: User's message
            stream: Whether to stream response

        Returns:
            Assistant's response text
        """
        if conversation_id not in self.conversations:
            self.create_conversation(conversation_id)

        conversation = self.conversations[conversation_id]
        conversation.add_message("user", user_message)

        if not self.is_available():
            # Fallback response when API not available
            response = self._fallback_response(user_message, conversation)
            conversation.add_message("assistant", response)
            return response

        try:
            if stream:
                return self._stream_response(conversation)
            else:
                return self._get_response(conversation)
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            conversation.add_message("assistant", response)
            return response

    def _get_response(self, conversation: Conversation) -> str:
        """Get non-streaming response from Claude"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.MAX_TOKENS,
            system=conversation.system_prompt,
            messages=conversation.get_messages_for_api()
        )

        assistant_message = response.content[0].text
        conversation.add_message("assistant", assistant_message)
        return assistant_message

    def _stream_response(self, conversation: Conversation) -> Generator[str, None, None]:
        """Stream response from Claude"""
        full_response = ""

        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.MAX_TOKENS,
            system=conversation.system_prompt,
            messages=conversation.get_messages_for_api()
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield text

        conversation.add_message("assistant", full_response)

    def _fallback_response(self, user_message: str, conversation: Conversation) -> str:
        """Generate fallback response when API is unavailable"""
        context = conversation.context

        # Check for assessment context
        if 'assessment_result' in context:
            result = context['assessment_result']
            score = result.get('overall_score', 0)
            maturity = result.get('maturity_level', 'Unknown')

            return f"""Thank you for your question. Based on your AI Readiness Assessment:

**Current State:**
- Overall Score: {score}/100
- Maturity Level: {maturity}

I'd be happy to provide more specific guidance, but I'm currently operating in offline mode. To get personalized AI-powered recommendations:

1. Ensure your ANTHROPIC_API_KEY environment variable is set
2. Restart the application

In the meantime, here are general recommendations based on your score:
- {"Focus on foundational capabilities: data governance, basic analytics, and executive buy-in" if score < 40 else ""}
- {"Scale successful pilots and invest in MLOps capabilities" if 40 <= score < 70 else ""}
- {"Optimize AI operations and explore advanced use cases" if score >= 70 else ""}

Would you like me to elaborate on any specific area?"""

        return """I'm currently operating in offline mode without access to the Claude API.

To enable full AI-powered consulting capabilities:
1. Set your ANTHROPIC_API_KEY environment variable
2. Restart the application

In the meantime, I can still help you with:
- Navigating the assessment questionnaire
- Understanding your results
- Exploring the framework templates

What would you like to explore?"""

    def generate_document(
        self,
        doc_type: str,
        context: Dict[str, Any],
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Generate a document using Claude.

        Args:
            doc_type: Type of document (strategy, governance, roadmap, etc.)
            context: Data to include in document
            custom_instructions: Additional instructions

        Returns:
            Generated document text
        """
        doc_prompts = {
            "strategy": "Generate an AI Strategy Document based on the assessment results.",
            "governance": "Generate an AI Governance Framework document.",
            "roadmap": "Generate a detailed AI Implementation Roadmap.",
            "executive_summary": "Generate an Executive Summary of the AI readiness assessment.",
            "business_case": "Generate an AI Business Case with ROI analysis.",
        }

        base_prompt = doc_prompts.get(doc_type, "Generate a document based on the provided context.")

        if custom_instructions:
            base_prompt += f"\n\nAdditional requirements:\n{custom_instructions}"

        # Create one-off conversation for document generation
        conv_id = f"doc_{doc_type}_{datetime.now().timestamp()}"
        self.create_conversation(conv_id, "document_writer", context)

        return self.chat(conv_id, base_prompt)

    def analyze_assessment(self, assessment_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze assessment results using Claude.

        Args:
            assessment_result: Assessment result dictionary

        Returns:
            Analysis with insights and recommendations
        """
        conv_id = f"analysis_{datetime.now().timestamp()}"
        self.create_conversation(conv_id, "analyst", {"assessment_result": assessment_result})

        analysis_prompt = """Analyze this AI readiness assessment and provide:

1. **Key Insights** (3-5 bullet points)
2. **Critical Gaps** requiring immediate attention
3. **Quick Wins** that can show early value
4. **Risk Areas** to monitor
5. **Recommended Next Steps** (prioritized)

Format your response as a structured analysis."""

        response = self.chat(conv_id, analysis_prompt)

        return {
            "analysis": response,
            "generated_at": datetime.now().isoformat(),
            "assessment_score": assessment_result.get("overall_score"),
            "maturity_level": assessment_result.get("maturity_level")
        }


# Singleton instance for easy import
_client: Optional[ClaudeClient] = None


def get_claude_client() -> ClaudeClient:
    """Get or create singleton Claude client"""
    global _client
    if _client is None:
        _client = ClaudeClient()
    return _client
