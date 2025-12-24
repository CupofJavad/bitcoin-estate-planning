# Database Migration Instructions - User Model

## Overview
Instructions for creating and running the database migration to add the User model for authentication.

---

## Prerequisites

1. **Virtual Environment Activated**
   ```bash
   cd backend
   source .venv/bin/activate
   ```

2. **Dependencies Installed**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Database Running**
   - PostgreSQL should be running (via Docker Compose)
   - Check: `docker-compose -f infra/docker/docker-compose.yml ps`

4. **Environment Variables**
   - Ensure `.env` file exists in `backend/` directory
   - Required variables: `SECRET_KEY`, `POSTGRES_*`, etc.

---

## Step 1: Install Dependencies

If you haven't already, install all dependencies including FastAPI Users:

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
pip install -e ".[dev]"
```

This will install:
- FastAPI Users
- All other backend dependencies
- Development dependencies

---

## Step 2: Create Migration

Generate the migration file for the User model:

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
alembic revision --autogenerate -m "add user model"
```

This will create a new migration file in `backend/alembic/versions/` with a name like:
- `xxxx_add_user_model.py`

**Expected Output:**
- Migration file created successfully
- No errors

---

## Step 3: Review Migration

Before running the migration, review the generated file:

```bash
# Find the latest migration file
ls -lt backend/alembic/versions/ | head -2

# Review the migration (replace with actual filename)
cat backend/alembic/versions/xxxx_add_user_model.py
```

**What to Check:**
- `create_table('users')` should be present
- Columns should include: `id`, `email`, `hashed_password`, `is_active`, `is_superuser`, `is_verified`, `full_name`, `created_at`, `updated_at`
- No unexpected table drops or modifications

---

## Step 4: Run Migration

Apply the migration to create the users table:

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
alembic upgrade head
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Running upgrade <previous> -> <new>, add user model
```

**Verify:**
```bash
# Connect to PostgreSQL and check
psql -h localhost -U postgres -d bitcoin_estate -c "\d users"
```

You should see the `users` table with all columns.

---

## Step 5: Verify Installation

Test that FastAPI Users is working:

```bash
cd /Users/Javad/Starter_Pack/bitcoin-estate-planning/backend
source .venv/bin/activate
python -c "from fastapi_users import FastAPIUsers; print('FastAPI Users installed successfully')"
```

---

## Troubleshooting

### Issue: "PermissionError: [Errno 1] Operation not permitted: '.env'"

**Solution:**
- Check file permissions: `ls -la backend/.env`
- Ensure you have read access
- If file doesn't exist, copy from `env.example`:
  ```bash
  cp backend/env.example backend/.env
  # Then edit .env with your values
  ```

### Issue: "Multiple top-level packages discovered"

**Solution:**
- This should be fixed in `pyproject.toml` with `[tool.setuptools]` section
- If still occurring, try:
  ```bash
  pip install --upgrade setuptools
  pip install -e ".[dev]"
  ```

### Issue: "ModuleNotFoundError: No module named 'fastapi_users'"

**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies:
  ```bash
  pip install -e ".[dev]"
  ```

### Issue: "alembic: command not found"

**Solution:**
- Ensure virtual environment is activated
- Install dependencies: `pip install -e ".[dev]"`
- Verify: `which alembic` should show path in `.venv/bin/`

### Issue: Database Connection Errors

**Solution:**
- Ensure PostgreSQL is running: `docker-compose -f infra/docker/docker-compose.yml ps`
- Check `.env` file has correct database credentials
- Test connection:
  ```bash
  psql -h localhost -U postgres -d bitcoin_estate -c "SELECT 1;"
  ```

---

## Next Steps

After successful migration:

1. **Test Registration**
   - Start backend: `uvicorn app.main:app --reload`
   - Test registration endpoint: `POST /api/v1/auth/register`

2. **Test Login**
   - Test login endpoint: `POST /api/v1/auth/jwt/login`

3. **Test Protected Endpoints**
   - Get JWT token from login
   - Test protected endpoint with `Authorization: Bearer <token>`

4. **Frontend Testing**
   - Install frontend dependencies: `cd frontend/client-portal && npm install`
   - Start frontend: `npm run dev`
   - Test registration and login flows

---

## Rollback (If Needed)

If you need to rollback the migration:

```bash
cd backend
source .venv/bin/activate
alembic downgrade -1
```

**Warning:** This will drop the `users` table and all user data!

---

**Last Updated**: December 2024

