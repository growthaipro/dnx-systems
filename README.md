# DNX Systems - AI-Powered Business Growth Platform

## Overview

DNX Systems is a comprehensive SaaS platform that connects customers with businesses, generates leads, automates marketing, and uses machine learning to improve results over time.

### Key Features

- **Lead Generation & Management**: Capture, track, score, and convert leads automatically
- **AI Marketing Suite**: Generate social media posts, ads, emails, landing pages, and blogs with AI
- **Advanced Analytics**: Real-time dashboards for revenue, leads, conversions, and customer growth
- **Machine Learning**: Lead conversion prediction, churn prediction, customer lifetime value, intelligent routing
- **Multi-Channel Notifications**: Email, SMS, WhatsApp, and push notifications
- **Role-Based Access Control**: Super Admin, Business Owner, Sales Executive, Customer roles
- **Enterprise Security**: JWT + OAuth authentication, encryption, audit logs, fraud detection

## Technology Stack

### Frontend
- **Next.js 14** - React framework with TypeScript
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - Data visualization
- **React Query** - State management
- **Axios** - HTTP client
- **Zustand** - Lightweight state management

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching and session management
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **JWT** - Authentication
- **OpenAI API** - AI content generation
- **Scikit-learn, XGBoost, TensorFlow** - Machine learning

### Infrastructure
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **PostgreSQL** - Data persistence
- **Redis** - Caching
- **S3-compatible storage** - File storage
- **Prometheus & Grafana** - Monitoring

## Project Structure

```
dnx-systems/
├── frontend/              # Next.js application
├── backend/               # FastAPI application
├── database/              # PostgreSQL migrations
├── kubernetes/            # K8s manifests
├── docker-compose.yml     # Local development setup
├── Dockerfile             # Docker image definition
└── docs/                  # Documentation
```

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+

### Local Development

```bash
# Clone the repository
git clone https://github.com/growthaipro/dnx-systems.git
cd dnx-systems

# Start all services with Docker Compose
docker-compose up -d

# Frontend runs on http://localhost:3000
# Backend API runs on http://localhost:8000
# API Docs available at http://localhost:8000/docs
```

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python -m alembic upgrade head
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Configuration

Create `.env` files in frontend and backend directories. See `.env.example` files for templates.

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Database Schema

Database migrations are managed with Alembic. Tables include:

- Users, Roles, Permissions
- Businesses, Business Profiles
- Leads, Lead Scores, Lead History
- Customers, Customer Interactions
- Subscriptions, Plans
- Analytics Events
- AI Content Generated Items
- Notifications Queue
- Audit Logs

## Authentication

- JWT-based authentication
- OAuth2 support (Google, Microsoft)
- OTP verification
- Password reset flows
- Role-based access control (RBAC)

## Deployment

### Docker Deployment
```bash
docker build -t dnx-systems:latest .
docker run -p 8000:8000 -p 3000:3000 dnx-systems:latest
```

### Kubernetes Deployment
```bash
kubectl apply -f kubernetes/
```

See `docs/DEPLOYMENT.md` for detailed instructions.

## Development Guidelines

- Follow PEP 8 for Python code
- Follow ESLint + Prettier for JavaScript/TypeScript
- Write unit tests for all features
- Document API endpoints with docstrings
- Use conventional commits

## Security

- All passwords are hashed with bcrypt
- JWT tokens are signed and validated
- CORS is configured for production
- SQL injection prevention with parameterized queries
- Rate limiting on all public endpoints
- HTTPS enforced in production
- GDPR compliance features included

## Monitoring & Logging

- Structured logging with Python logging module
- Request/response logging
- Error tracking with Sentry integration
- Performance monitoring with Prometheus
- Dashboard visualization with Grafana

## Contributing

1. Create a feature branch
2. Follow coding standards
3. Write tests
4. Submit pull request
5. Code review required

## License

Proprietary - All rights reserved

## Support

For issues and feature requests, open a GitHub issue.

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-05  
**Status**: Production Ready
