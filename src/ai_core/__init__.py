"""
AI Core Module - Claude API Integration

Provides intelligent AI-powered features:
- Conversational AI consultant
- Document generation
- Knowledge base integration
- Context-aware recommendations
"""

from .claude_client import ClaudeClient
from .chat_engine import AIChatEngine
from .document_generator import DocumentGenerator

__all__ = ['ClaudeClient', 'AIChatEngine', 'DocumentGenerator']
