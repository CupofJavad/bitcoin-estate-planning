# Bitcoin Estate Planning Platform - MVP

A comprehensive platform for Bitcoin-native estate planning with timelock policies, beneficiary management, and automated inheritance workflows.

## Architecture

- **Backend**: FastAPI (Python 3.12) with PostgreSQL
- **Frontend**: Next.js 15+ with TypeScript
- **Blockchain**: Bitcoin testnet/mock integration
- **Database**: PostgreSQL 15+
- **Cache**: Redis

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Node.js 18+

### Development Setup

1. Clone the repository
2. Copy `backend/env.example` to `backend/.env` and configure
3. Start services:
   ```bash
   docker-compose -f infra/docker/docker-compose.yml up -d
   ```
4. Set up backend:
   ```bash
   cd backend
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```
5. Run migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```
6. Start backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
7. Set up frontend:
   ```bash
   cd frontend/client-portal
   npm install
   ```
8. Start frontend:
   ```bash
   cd frontend/client-portal
   npm run dev
   ```

## Project Structure

```
bitcoin-estate-planning/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   └── schemas/     # Pydantic schemas
│   ├── alembic/         # Database migrations
│   └── pyproject.toml
├── frontend/            # Next.js frontend applications
│   └── client-portal/   # Main client portal
├── infra/               # Docker and infrastructure configuration
│   └── docker/
└── docs/                # Documentation
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Estate Plans
- `GET /api/v1/estate-plans` - List all estate plans
- `GET /api/v1/estate-plans/{id}` - Get estate plan with relations
- `POST /api/v1/estate-plans` - Create estate plan
- `PATCH /api/v1/estate-plans/{id}` - Update estate plan
- `DELETE /api/v1/estate-plans/{id}` - Delete estate plan

### Beneficiaries
- `GET /api/v1/beneficiaries` - List all beneficiaries
- `GET /api/v1/beneficiaries/{id}` - Get beneficiary
- `POST /api/v1/beneficiaries` - Create beneficiary
- `PATCH /api/v1/beneficiaries/{id}` - Update beneficiary
- `DELETE /api/v1/beneficiaries/{id}` - Delete beneficiary

### Timelock Policies
- `GET /api/v1/timelock-policies` - List all timelock policies
- `GET /api/v1/timelock-policies/{id}` - Get timelock policy
- `POST /api/v1/timelock-policies` - Create timelock policy
- `PATCH /api/v1/timelock-policies/{id}` - Update timelock policy
- `DELETE /api/v1/timelock-policies/{id}` - Delete timelock policy

## Environment Variables

See `backend/env.example` for required environment variables.

## License

Proprietary

