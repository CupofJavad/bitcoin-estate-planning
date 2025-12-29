"""Chatbot API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.chatbot import get_chatbot_service, ChatbotService
from app.core.users import current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


async def get_demo_user(
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Temporary helper for local testing:
    return the first user in the database as the current user.
    """
    result = await db.execute(select(User).order_by(User.id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No users found in database for demo mode",
        )
    return user


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    model: Optional[str] = None
    error: Optional[str] = None
    timestamp: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    user: User = Depends(get_demo_user),
):
    """Send a message to the chatbot and get a response.

    **Features:**
    - Context-aware responses based on conversation history
    - Estate planning specific knowledge
    - Rate limiting (should be implemented at application level)

    **Rate Limits:**
    - Recommended: 10 requests per minute per user
    """
    try:
        # Convert conversation history to dict format
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]

        # Get response from chatbot
        result = await chatbot_service.get_response(
            request.message, conversation_history=history
        )

        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}",
        )


@router.get("/suggestions", response_model=List[str])
async def get_suggestions(
    chatbot_service: ChatbotService = Depends(get_chatbot_service),
    user: User = Depends(get_demo_user),
):
    """Get suggested questions for the chatbot.

    Returns a list of helpful questions users can ask.
    """
    return chatbot_service.get_suggested_questions()

