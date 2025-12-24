"""Database models."""

from app.models.user import User
from app.models.estate_plan import EstatePlan
from app.models.beneficiary import Beneficiary
from app.models.timelock_policy import TimelockPolicy

__all__ = ["User", "EstatePlan", "Beneficiary", "TimelockPolicy"]

from app.models.estate_plan import EstatePlan
from app.models.beneficiary import Beneficiary
from app.models.timelock_policy import TimelockPolicy

__all__ = ["EstatePlan", "Beneficiary", "TimelockPolicy"]

