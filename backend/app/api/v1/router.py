"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    estate_plans,
    beneficiaries,
    timelock_policies,
    bitcoin,
    auth,
    logs,
    chatbot,
)

api_router = APIRouter()

# Authentication routes (public)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Protected routes
api_router.include_router(estate_plans.router, prefix="/estate-plans", tags=["estate-plans"])
api_router.include_router(beneficiaries.router, prefix="/beneficiaries", tags=["beneficiaries"])
api_router.include_router(
    timelock_policies.router, prefix="/timelock-policies", tags=["timelock-policies"]
)
api_router.include_router(bitcoin.router, prefix="/bitcoin", tags=["bitcoin"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(logs.router, tags=["logs"])

