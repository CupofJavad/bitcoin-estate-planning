"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import estate_plans, beneficiaries, timelock_policies

api_router = APIRouter()

api_router.include_router(estate_plans.router, prefix="/estate-plans", tags=["estate-plans"])
api_router.include_router(beneficiaries.router, prefix="/beneficiaries", tags=["beneficiaries"])
api_router.include_router(
    timelock_policies.router, prefix="/timelock-policies", tags=["timelock-policies"]
)

