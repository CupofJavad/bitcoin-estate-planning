# Bitcoin Estate Planning Platform

<div align="center">

![Bitcoin Estate Planning Platform](docs/images/dashboard-screenshot.png)

*Secure, automated Bitcoin inheritance planning with timelock policies and beneficiary management*

[![Version](https://img.shields.io/badge/version-1.01-blue.svg)](https://github.com/yourusername/bitcoin-estate-planning/releases/tag/v1.01)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org/)

</div>

---

## 📋 Table of Contents

- [Vision](#-vision)
- [Objectives](#-objectives)
- [Features](#-features)
- [Current Status](#-current-status)
- [Development Timeline](#-development-timeline)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Vision

**Bitcoin Estate Planning Platform** is a comprehensive, user-friendly solution designed to solve one of the most critical challenges in Bitcoin adoption: **secure and automated inheritance planning**.

### The Problem

Bitcoin's decentralized nature means traditional estate planning methods don't apply. Private keys must be secured, but also accessible to heirs. Without proper planning, Bitcoin assets can be permanently lost, creating a significant barrier to adoption.

### Our Solution

A modern, web-based platform that enables Bitcoin holders to:
- **Plan their Bitcoin inheritance** with confidence
- **Automate asset distribution** through timelock policies
- **Manage beneficiaries** with clear allocation strategies
- **Ensure security** while maintaining accessibility for heirs

### Why It Matters

As Bitcoin adoption grows, millions of holders need tools to ensure their digital assets can be safely passed to future generations. This platform bridges the gap between Bitcoin's technical complexity and the need for accessible estate planning tools.

---

## 🎯 Objectives

### Primary Objectives

1. **Simplify Bitcoin Estate Planning**
   - Provide an intuitive, browser-based interface
   - Eliminate technical barriers for non-technical users
   - Guide users through the estate planning process

2. **Ensure Security & Accessibility**
   - Secure storage of estate planning data
   - Clear instructions for beneficiaries
   - Automated timelock policy execution

3. **Enable Automated Inheritance**
   - Timelock policies for conditional asset release
   - Multiple trigger conditions (death, inactivity, manual)
   - Flexible beneficiary allocation strategies

4. **Build Investor Confidence**
   - Professional, polished user experience
   - Comprehensive documentation
   - Scalable, production-ready architecture

### Success Metrics

- ✅ Complete CRUD operations via browser (no API knowledge required)
- ✅ Professional UI/UX that impresses investors
- ✅ All features functional and tested
- ✅ Ready for production deployment
- ✅ Comprehensive documentation and testing

---

## ✨ Features

### Core Features (v1.01 - Current)

#### 🏛️ Estate Plans Management
- **Create Estate Plans**: Set up new Bitcoin estate plans with custom names, descriptions, and Bitcoin addresses
- **View & Edit**: Full CRUD operations for estate plans
- **Status Management**: Active/Inactive status tracking
- **Search & Filter**: Quickly find estate plans by name or description
- **Detail View**: Comprehensive estate plan overview with statistics

#### 👥 Beneficiary Management
- **Add Beneficiaries**: Assign beneficiaries to estate plans with allocation percentages
- **Allocation Visualization**: Interactive pie charts showing distribution
- **Smart Validation**: Prevents over-allocation (>100%) with real-time feedback
- **Contact Information**: Store email addresses and Bitcoin addresses for beneficiaries
- **Edit & Delete**: Full management capabilities

#### ⏰ Timelock Policies
- **Policy Creation**: Define timelock policies with block counts and trigger conditions
- **Block Calculator**: Automatic conversion of blocks to days (~144 blocks/day)
- **Trigger Conditions**: Support for death, inactivity, manual, and date-based triggers
- **Active/Inactive Toggle**: Enable or disable policies as needed
- **Policy Management**: Full CRUD operations

#### 📊 Dashboard & Analytics
- **Statistics Overview**: Quick view of beneficiaries, allocations, and policies
- **Visual Charts**: Allocation distribution pie charts
- **Real-time Updates**: Statistics update automatically as data changes

#### 🎨 User Experience
- **Modern UI**: Clean, professional design with Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Toast Notifications**: User-friendly feedback for all actions
- **Loading States**: Clear indicators during API calls
- **Error Handling**: Graceful error messages and recovery
- **Form Validation**: Real-time validation with helpful error messages

### Planned Features (Future Versions)

- 🔐 **Authentication & User Management**: Multi-user support with secure login
- 🤖 **AI Chatbot**: Intelligent assistance for estate planning questions
- 📧 **Email Notifications**: Automated alerts and reminders
- 📄 **Export & Reports**: PDF generation for estate plans
- 🔗 **Bitcoin Integration**: Real balance checking and address validation
- 📱 **Mobile App**: Native iOS/Android applications
- 🌐 **Multi-language Support**: Internationalization

---

## 📍 Current Status

### Version 1.01 - Investor Demo Ready ✅

**Release Date:** December 2025  
**Branch:** `feature/investor-demo-v1`  
**Tag:** `v1.01`

#### Completed ✅

- ✅ **Backend API**: Complete FastAPI backend with PostgreSQL
- ✅ **Frontend UI**: Full Next.js 15+ application with TypeScript
- ✅ **Estate Plans**: Complete CRUD via browser interface
- ✅ **Beneficiaries**: Full management with allocation validation
- ✅ **Timelock Policies**: Complete policy management system
- ✅ **UI Components**: Professional, investor-ready interface
- ✅ **Data Visualization**: Charts and statistics
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Testing Documentation**: 24 user stories, test plans, checklists
- ✅ **API Integration**: All frontend-backend connections verified

#### In Progress 🚧

- 🚧 **Authentication**: User management system (Phase 2)
- 🚧 **Chatbot**: AI-powered assistance (Phase 3)
- 🚧 **Deployment**: Production server setup (Phase 4)

#### Planned 📋

- 📋 **Advanced Features**: Bitcoin balance checking, email notifications
- 📋 **Analytics**: Usage tracking and reporting
- 📋 **Documentation**: User guides and enhanced API docs

---

## 📅 Development Timeline

### Phase 0: MVP Foundation ✅ (Completed)
**Duration:** Initial development  
**Status:** ✅ Complete

- FastAPI backend with PostgreSQL
- Basic Next.js frontend
- Docker Compose infrastructure
- CRUD API endpoints
- Database migrations

### Phase 1: Complete Frontend UX ✅ (Completed)
**Duration:** Weeks 1-2  
**Status:** ✅ Complete (v1.01)

- ✅ Estate Plans management UI
- ✅ Beneficiaries management UI
- ✅ Timelock Policies management UI
- ✅ Dashboard with statistics
- ✅ Professional UI/UX design
- ✅ Form validation and error handling
- ✅ Responsive design

**Current Position:** ✅ **Phase 1 Complete**

### Phase 2: Authentication & User Management 🚧 (In Progress)
**Duration:** Weeks 2-3  
**Status:** 🚧 Planned

- User registration and login
- JWT token authentication
- Protected routes
- User profile management
- Multi-user support

### Phase 3: Chatbot Integration 📋 (Planned)
**Duration:** Weeks 3-4  
**Status:** 📋 Planned

- AI-powered chatbot backend
- Chat interface component
- Estate planning guidance
- Conversation history

### Phase 4: Deployment & Infrastructure 📋 (Planned)
**Duration:** Weeks 4-5  
**Status:** 📋 Planned

- Production Docker setup
- Server deployment (DigitalOcean/AWS/Railway)
- Domain and SSL configuration
- CI/CD pipeline

### Phase 5: Investor Demo Features 📋 (Planned)
**Duration:** Weeks 5-6  
**Status:** 📋 Planned

- Demo data seeding
- Advanced features (Bitcoin integration)
- Analytics and reporting
- Enhanced documentation

### Phase 6: Testing & Polish 📋 (Planned)
**Duration:** Week 6  
**Status:** 📋 Planned

- Comprehensive testing (unit, integration, E2E)
- Performance optimization
- Bug fixes and refinements
- Security audit

---

## 📸 Screenshots

### Dashboard - Estate Plans List

![Estate Plans Dashboard](docs/images/dashboard-screenshot.png)

*The main dashboard showing estate plans with search functionality and create button. Each estate plan card displays status, Bitcoin address, and action buttons.*

### Estate Plan Detail Page

![Estate Plan Details](docs/images/detail-page-screenshot.png)

*Comprehensive estate plan detail view showing statistics, beneficiaries section, and timelock policies. The page includes allocation charts and policy management.*

---

## 🏗️ Architecture

### Technology Stack

#### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Cache**: Redis
- **API Docs**: Swagger/OpenAPI

#### Frontend
- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v3
- **Forms**: React Hook Form + Zod
- **State**: TanStack Query + Zustand
- **Charts**: Recharts
- **Icons**: Lucide React

#### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL (containerized)
- **Cache**: Redis (containerized)
- **Development**: Hot reload for both frontend and backend

### System Architecture

```
┌─────────────────┐
│   Next.js UI    │  ← User Interface (Port 3000/3001)
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI API   │  ← Backend Service (Port 8000)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────┐
│Postgres│ │Redis │  ← Data Layer
└────────┘ └──────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Python** 3.12+
- **Node.js** 18+
- **Git**

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bitcoin-estate-planning.git
   cd bitcoin-estate-planning
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose -f infra/docker/docker-compose.yml up -d
   ```

3. **Set up backend**
   ```bash
   cd backend
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start backend server**
   ```bash
   uvicorn app.main:app --reload
   ```
   Backend will be available at: http://localhost:8000

7. **Set up frontend** (in a new terminal)
   ```bash
   cd frontend/client-portal
   npm install
   cp env.example .env.local
   # Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

8. **Start frontend**
   ```bash
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

### Using Makefile

For convenience, use the provided Makefile:

```bash
# Bootstrap entire project
make bootstrap

# Start services
make start-services

# Setup backend
make setup-backend

# Setup frontend
make setup-frontend

# Run migrations
make migrate

# Start backend dev server
make dev-backend

# Start frontend dev server
make dev-frontend
```

---

## 📁 Project Structure

```
bitcoin-estate-planning/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/  # Individual endpoint modules
│   │   │       └── router.py    # API router
│   │   ├── core/           # Core configuration
│   │   │   ├── config.py   # Settings and environment
│   │   │   ├── database.py # Database connection
│   │   │   └── redis.py    # Redis client
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # FastAPI application
│   ├── alembic/            # Database migrations
│   ├── tests/              # Test suite
│   └── pyproject.toml      # Python dependencies
│
├── frontend/
│   └── client-portal/      # Next.js frontend application
│       ├── app/            # Next.js App Router pages
│       ├── components/     # React components
│       │   ├── estate-plan/
│       │   ├── beneficiary/
│       │   ├── timelock-policy/
│       │   └── ui/         # Reusable UI components
│       ├── lib/            # Utilities and API client
│       └── package.json    # Node.js dependencies
│
├── infra/                  # Infrastructure configuration
│   └── docker/
│       └── docker-compose.yml
│
├── docs/                   # Documentation
│   ├── USER_STORIES.md     # 24 user stories
│   ├── TESTING_PLAN.md     # Testing documentation
│   ├── ROADMAP.md          # Development roadmap
│   └── ...
│
├── scripts/                # Utility scripts
│   ├── test_api.sh         # API testing script
│   └── test_frontend_backend.sh  # Integration tests
│
├── Makefile                # Development commands
├── LICENSE                 # Proprietary license
└── README.md              # This file
```

---

## 📚 API Documentation

### Interactive API Docs

Once the backend is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Estate Plans
- `GET /api/v1/estate-plans` - List all estate plans
- `GET /api/v1/estate-plans/{id}` - Get estate plan with relations
- `POST /api/v1/estate-plans` - Create estate plan
- `PATCH /api/v1/estate-plans/{id}` - Update estate plan
- `DELETE /api/v1/estate-plans/{id}` - Delete estate plan

#### Beneficiaries
- `GET /api/v1/beneficiaries` - List all beneficiaries
- `GET /api/v1/beneficiaries?estate_plan_id={id}` - Filter by estate plan
- `GET /api/v1/beneficiaries/{id}` - Get beneficiary
- `POST /api/v1/beneficiaries` - Create beneficiary
- `PATCH /api/v1/beneficiaries/{id}` - Update beneficiary
- `DELETE /api/v1/beneficiaries/{id}` - Delete beneficiary

#### Timelock Policies
- `GET /api/v1/timelock-policies` - List all timelock policies
- `GET /api/v1/timelock-policies?estate_plan_id={id}` - Filter by estate plan
- `GET /api/v1/timelock-policies/{id}` - Get timelock policy
- `POST /api/v1/timelock-policies` - Create timelock policy
- `PATCH /api/v1/timelock-policies/{id}` - Update timelock policy
- `DELETE /api/v1/timelock-policies/{id}` - Delete timelock policy

---

## 🧪 Testing

### Automated Tests

#### API Tests
```bash
./scripts/test_api.sh
```

#### Integration Tests
```bash
./scripts/test_frontend_backend.sh
```

#### Python Tests
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

### Manual Testing

See comprehensive testing documentation:
- [User Stories](docs/USER_STORIES.md) - 24 user stories with acceptance criteria
- [Testing Plan](docs/TESTING_PLAN.md) - Detailed test cases
- [Manual Testing Checklist](docs/MANUAL_TESTING_CHECKLIST.md) - Step-by-step guide
- [Debugging Checklist](docs/DEBUGGING_CHECKLIST.md) - Systematic debugging approach

---

## 🌿 Branch Strategy

### Current Branch: `feature/investor-demo-v1`

**Version 1.01** is tagged and preserved. Future development should occur on new branches.

### Branch Naming Convention

- `main` - Production-ready code (protected)
- `develop` - Integration branch for features
- `feature/*` - New features (e.g., `feature/authentication`)
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `release/*` - Release preparation branches

### Version Tags

- `v1.01` - Current stable version (Investor Demo Ready)
- Future versions will follow semantic versioning (v1.02, v2.0.0, etc.)

### Workflow

1. **Create feature branch** from `develop` or `main`
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Develop and commit** changes
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. **Push and create PR** to `develop` or `main`

4. **Tag releases** when ready
   ```bash
   git tag -a v1.02 -m "Version 1.02 - New features"
   git push origin v1.02
   ```

---

## 🤝 Contributing

This is currently a proprietary project. For internal contributors:

1. Follow the branch strategy above
2. Write tests for new features
3. Update documentation
4. Follow code style guidelines
5. Create pull requests for review

---

## 📄 License

**Proprietary** - All rights reserved.

This software and associated documentation files are proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited.

---

## 📞 Contact & Support

For questions, issues, or contributions, please contact the development team.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- And many other open-source libraries

---

<div align="center">

**Bitcoin Estate Planning Platform** - Secure, Automated Bitcoin Inheritance Planning

[Version 1.01](https://github.com/yourusername/bitcoin-estate-planning/releases/tag/v1.01) | [Documentation](docs/) | [Roadmap](docs/ROADMAP.md)

</div>
