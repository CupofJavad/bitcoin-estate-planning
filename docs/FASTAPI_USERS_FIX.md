# FastAPI Users v15 Import Fix

## Issue
When running `alembic revision --autogenerate`, the following error occurred:
```
sqlalchemy.exc.ArgumentError: Mapper Mapper[User(users)] could not assemble any primary key columns for mapped table 'users'
```

## Root Cause
FastAPI Users v15 changed the import paths. The `SQLAlchemyBaseUserTable` and `SQLAlchemyUserDatabase` are now in the `fastapi_users_db_sqlalchemy` package, not `fastapi_users.db`.

## Solution

### 1. Updated User Model (`backend/app/models/user.py`)
Changed import from:
```python
from fastapi_users.db import SQLAlchemyBaseUserTable
```

To:
```python
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
```

### 2. Updated Users Configuration (`backend/app/core/users.py`)
Changed import from:
```python
from fastapi_users.db import SQLAlchemyUserDatabase
```

To:
```python
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
```

### 3. Updated Alembic Environment (`backend/alembic/env.py`)
Added User model to imports:
```python
from app.models import EstatePlan, Beneficiary, TimelockPolicy, User  # noqa: F401
```

## Verification

After these changes, you should be able to:

1. **Test User Model Import:**
   ```bash
   cd backend
   source .venv/bin/activate
   python -c "from app.models.user import User; print('User model imported successfully')"
   ```

2. **Create Migration:**
   ```bash
   alembic revision --autogenerate -m "add user model"
   ```

3. **Run Migration:**
   ```bash
   alembic upgrade head
   ```

## FastAPI Users v15 Changes

- `fastapi-users[sqlalchemy]` now installs `fastapi-users-db-sqlalchemy` as a separate package
- Import paths changed from `fastapi_users.db` to `fastapi_users_db_sqlalchemy`
- The base table classes remain functionally the same

## References

- FastAPI Users v15 Documentation: https://fastapi-users.github.io/fastapi-users/
- Migration Guide: Check FastAPI Users changelog for v15

---

**Last Updated**: December 2024

