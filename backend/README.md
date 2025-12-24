# Bitcoin Estate Planning Platform - Backend

FastAPI backend for Bitcoin-native estate planning.

## Setup

1. Create virtual environment:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Copy `.env.example` to `.env` and configure

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

