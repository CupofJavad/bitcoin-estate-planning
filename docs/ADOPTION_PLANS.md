# Adoption Plans - Detailed Implementation Guides

## Overview
Detailed step-by-step implementation plans for adopting identified solutions from repository findings.

---

## Plan 1: Authentication System (Phase 2)

### Decision: FastAPI Users + NextAuth.js

**Rationale:**
- FastAPI Users: Production-ready, saves 2-3 weeks
- NextAuth.js: Industry standard, excellent docs
- Combined: Complete auth solution

### Backend Implementation (FastAPI Users)

#### Step 1: Installation
```bash
cd backend
source .venv/bin/activate
pip install fastapi-users[sqlalchemy,oauth]
```

#### Step 2: User Model Setup
```python
# backend/app/models/user.py
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Boolean
from app.core.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    
    # Additional fields
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
```

#### Step 3: Database Migration
```bash
alembic revision --autogenerate -m "add user model"
alembic upgrade head
```

#### Step 4: FastAPI Users Configuration
```python
# backend/app/core/users.py
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from app.models.user import User
from app.core.database import get_async_session

jwt_authentication = JWTAuthentication(
    secret=SECRET_KEY,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [jwt_authentication],
)

# Add to router
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)
```

#### Step 5: Protected Routes
```python
# backend/app/api/v1/endpoints/estate_plans.py
from fastapi_users import FastAPIUsers

@router.get("/estate-plans")
async def list_estate_plans(
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db)
):
    # User is authenticated
    return await estate_plans_service.list(user.id, db)
```

**Estimated Time**: 1-2 weeks  
**Time Saved**: 2-3 weeks

---

### Frontend Implementation (NextAuth.js)

#### Step 1: Installation
```bash
cd frontend/client-portal
npm install next-auth
```

#### Step 2: NextAuth Configuration
```typescript
// frontend/client-portal/app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/jwt/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: credentials.email,
            password: credentials.password,
          }),
        })
        const user = await res.json()
        if (user && res.ok) {
          return user
        }
        return null
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.access_token
      }
      return token
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken
      return session
    }
  },
  pages: {
    signIn: '/login',
  }
}

export default NextAuth(authOptions)
```

#### Step 3: Protected Routes Middleware
```typescript
// frontend/client-portal/middleware.ts
import { withAuth } from 'next-auth/middleware'

export default withAuth({
  pages: {
    signIn: '/login',
  }
})

export const config = {
  matcher: ['/estate-plans/:path*', '/dashboard/:path*']
}
```

#### Step 4: Login Page
```typescript
// frontend/client-portal/app/login/page.tsx
'use client'

import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const result = await signIn('credentials', {
      email: e.target.email.value,
      password: e.target.password.value,
      redirect: false,
    })
    if (result?.ok) {
      router.push('/')
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Login form */}
    </form>
  )
}
```

**Estimated Time**: 1 week  
**Time Saved**: 1-2 weeks

---

## Plan 2: Email Notifications (Phase 3)

### Implementation: FastAPI-Mail + SendGrid

#### Step 1: Installation
```bash
cd backend
pip install fastapi-mail jinja2
```

#### Step 2: Configuration
```python
# backend/app/core/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.sendgrid.net",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

fm = FastMail(conf)
```

#### Step 3: Email Templates
```html
<!-- backend/app/templates/emails/estate_plan_created.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Estate Plan Created</title>
</head>
<body>
    <h1>Your Estate Plan Has Been Created</h1>
    <p>Hello {{ user.name }},</p>
    <p>Your estate plan "{{ estate_plan.name }}" has been successfully created.</p>
    <p>You can view it <a href="{{ estate_plan_url }}">here</a>.</p>
</body>
</html>
```

#### Step 4: Email Service
```python
# backend/app/services/email_service.py
from fastapi_mail import MessageSchema
from jinja2 import Template
from app.core.email import fm
import os

async def send_estate_plan_created_email(user, estate_plan):
    template_path = "app/templates/emails/estate_plan_created.html"
    with open(template_path) as f:
        template = Template(f.read())
    
    html = template.render(
        user=user,
        estate_plan=estate_plan,
        estate_plan_url=f"{settings.FRONTEND_URL}/estate-plans/{estate_plan.id}"
    )
    
    message = MessageSchema(
        subject="Estate Plan Created",
        recipients=[user.email],
        body=html,
        subtype="html"
    )
    
    await fm.send_message(message)
```

#### Step 5: Integration
```python
# backend/app/api/v1/endpoints/estate_plans.py
from app.services.email_service import send_estate_plan_created_email

@router.post("/estate-plans")
async def create_estate_plan(
    estate_plan: EstatePlanCreate,
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db)
):
    created = await estate_plans_service.create(estate_plan, user.id, db)
    
    # Send email notification
    await send_estate_plan_created_email(user, created)
    
    return created
```

**Estimated Time**: 1 week  
**Time Saved**: 1-2 weeks

---

## Plan 3: PDF Generation (Phase 5)

### Implementation: WeasyPrint + Jinja2

#### Step 1: Installation
```bash
cd backend
pip install weasyprint jinja2
```

#### Step 2: PDF Template
```html
<!-- backend/app/templates/pdf/estate_plan.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background: #F7931A; color: white; padding: 20px; }
        .section { margin: 20px 0; }
        .beneficiary { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ estate_plan.name }}</h1>
    </div>
    
    <div class="section">
        <h2>Description</h2>
        <p>{{ estate_plan.description }}</p>
    </div>
    
    <div class="section">
        <h2>Beneficiaries</h2>
        {% for beneficiary in estate_plan.beneficiaries %}
        <div class="beneficiary">
            <h3>{{ beneficiary.name }}</h3>
            <p>Allocation: {{ beneficiary.allocation_percentage }}%</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

#### Step 3: PDF Service
```python
# backend/app/services/pdf_service.py
from weasyprint import HTML
from jinja2 import Template
from app.core.config import settings
import os

async def generate_estate_plan_pdf(estate_plan):
    template_path = "app/templates/pdf/estate_plan.html"
    with open(template_path) as f:
        template = Template(f.read())
    
    html_content = template.render(estate_plan=estate_plan)
    pdf = HTML(string=html_content).write_pdf()
    
    return pdf
```

#### Step 4: PDF Endpoint
```python
# backend/app/api/v1/endpoints/estate_plans.py
from fastapi.responses import Response
from app.services.pdf_service import generate_estate_plan_pdf

@router.get("/estate-plans/{id}/pdf")
async def export_estate_plan_pdf(
    id: int,
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db)
):
    estate_plan = await estate_plans_service.get(id, user.id, db)
    pdf = await generate_estate_plan_pdf(estate_plan)
    
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=estate_plan_{id}.pdf"}
    )
```

**Estimated Time**: 1 week  
**Time Saved**: 1-2 weeks

---

## Plan 4: Deployment (Phase 4)

### Implementation: Docker Production

#### Step 1: Production Dockerfile (Backend)
```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: Production Dockerfile (Frontend)
```dockerfile
# frontend/client-portal/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

#### Step 3: Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend/client-portal
    environment:
      NEXT_PUBLIC_API_URL: ${API_URL}
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

**Estimated Time**: 1 week  
**Time Saved**: 1 week

---

## 📊 Implementation Timeline

### Phase 2: Authentication (Weeks 1-3)
- Week 1: Backend (FastAPI Users)
- Week 2: Frontend (NextAuth.js)
- Week 3: Testing & integration

### Phase 3: Email (Week 4)
- Week 4: Email notifications implementation

### Phase 4: Deployment (Week 5)
- Week 5: Docker production setup

### Phase 5: PDF (Week 6)
- Week 6: PDF generation

**Total Estimated Time**: 6 weeks  
**Total Time Saved**: 5-8 weeks

---

## ✅ Success Criteria

### Authentication
- [ ] Users can register
- [ ] Users can login
- [ ] Protected routes work
- [ ] JWT tokens refresh
- [ ] Logout works

### Email
- [ ] Emails send successfully
- [ ] Templates render correctly
- [ ] Notifications trigger on events

### PDF
- [ ] PDFs generate correctly
- [ ] Templates are styled
- [ ] Download works

### Deployment
- [ ] Docker builds succeed
- [ ] Services start correctly
- [ ] Production environment works

---

## 🔄 Next Actions

1. **Review Plans**: Team review of adoption plans
2. **Prioritize**: Decide which to implement first
3. **Execute**: Begin Phase 2 implementation
4. **Document**: Update as implementation progresses

