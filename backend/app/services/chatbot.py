"""Chatbot service for estate planning assistance.

Provides AI-powered assistance for Bitcoin estate planning questions.
Uses OpenAI API with fallback support for other providers.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class ChatbotService:
    """Service for handling chatbot conversations."""

    SYSTEM_PROMPT = """You are a helpful assistant for Bitcoin estate planning. 
You help users understand:
- How to set up Bitcoin estate plans
- How timelock policies work
- How to allocate assets to beneficiaries
- Bitcoin inheritance best practices
- Security considerations for Bitcoin estate planning

Be concise, helpful, and accurate. If you don't know something, say so.
Always prioritize security and best practices."""

    def __init__(self):
        """Initialize chatbot service."""
        self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        self.model = getattr(settings, 'CHATBOT_MODEL', 'gpt-3.5-turbo')
        self.max_tokens = getattr(settings, 'CHATBOT_MAX_TOKENS', 500)
        self.temperature = getattr(settings, 'CHATBOT_TEMPERATURE', 0.7)

    async def get_response(
        self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, any]:
        """Get chatbot response to a message.

        Args:
            message: User's message
            conversation_history: Previous messages in the conversation

        Returns:
            Dictionary with response and metadata
        """
        if not self.api_key:
            return {
                "response": "Chatbot is not configured. Please set OPENAI_API_KEY environment variable.",
                "error": "API key not configured",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        try:
            # Build messages list
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Limit to last 10 messages

            # Add current message
            messages.append({"role": "user", "content": message})

            # Call OpenAI API
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                    },
                )
                response.raise_for_status()
                data = response.json()

                # Extract response
                assistant_message = data["choices"][0]["message"]["content"]

                return {
                    "response": assistant_message,
                    "model": self.model,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }

        except httpx.HTTPStatusError as e:
            logger.error(f"OpenAI API error: {e.response.status_code} - {e.response.text}")
            return {
                "response": "I'm having trouble connecting to the AI service. Please try again later.",
                "error": f"API error: {e.response.status_code}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        except Exception as e:
            logger.error(f"Chatbot error: {str(e)}")
            return {
                "response": "An error occurred while processing your message. Please try again.",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    def get_suggested_questions(self) -> List[str]:
        """Get suggested questions for users.

        Returns:
            List of suggested questions
        """
        return [
            "What is a Bitcoin timelock?",
            "How do I set up an estate plan?",
            "What happens when a timelock activates?",
            "How do I allocate assets to beneficiaries?",
            "What are best practices for Bitcoin inheritance?",
        ]


# Global service instance
_chatbot_service: Optional[ChatbotService] = None


def get_chatbot_service() -> ChatbotService:
    """Get chatbot service instance."""
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service

