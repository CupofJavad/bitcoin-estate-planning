.PHONY: help setup-backend setup-frontend start-services stop-services migrate dev-backend dev-frontend

help:
	@echo "Available commands:"
	@echo "  make setup-backend     - Set up Python backend environment"
	@echo "  make setup-frontend    - Set up Node.js frontend"
	@echo "  make start-services    - Start PostgreSQL and Redis via Docker"
	@echo "  make stop-services     - Stop Docker services"
	@echo "  make migrate           - Run database migrations"
	@echo "  make dev-backend       - Start backend development server"
	@echo "  make dev-frontend      - Start frontend development server"

setup-backend:
	@echo "Setting up backend..."
	cd backend && python3.12 -m venv .venv
	cd backend && . .venv/bin/activate && pip install -e ".[dev]"

setup-frontend:
	@echo "Setting up frontend..."
	cd frontend/client-portal && npm install

start-services:
	@echo "Starting Docker services..."
	docker-compose -f infra/docker/docker-compose.yml up -d
	@echo "Waiting for services to be ready..."
	@sleep 5

stop-services:
	@echo "Stopping Docker services..."
	docker-compose -f infra/docker/docker-compose.yml down

migrate:
	@echo "Running database migrations..."
	cd backend && . .venv/bin/activate && alembic upgrade head

dev-backend:
	@echo "Starting backend server..."
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload

dev-frontend:
	@echo "Starting frontend server..."
	cd frontend/client-portal && npm run dev

