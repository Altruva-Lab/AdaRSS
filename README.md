
# AdaRSS: Adaptive Representation Systems for Structured Skilled Data

> *"End skill instability. Build careers that last."*
AdaRSS is building the world's first Career Stability Intelligence Layer that helps individuals, institutions, and governments identify which skills create durable careers in a rapidly changing economy.

---

## 🚀 The Vision

Tech skills have become a moving target. Developers in the Global South—and everywhere—invest years learning frameworks that become obsolete in 18 months. Bootcamps chase buzzwords. HR departments post "must-have" skills that fade before the job posting expires. The result: burnout, wasted potential, and broken careers.

AdaRSS is the intelligence layer that solves this. We've built an **open-source AI system** that reads the global job market and classifies skills into three categories:

| Label | Category | Example |
|-------|----------|---------|
| **0** | **Enduring foundations** | SQL, REST APIs, Data Structures, Systems Thinking |
| **1** | **Emergent necessities** | MLOps, Kubernetes, Transformer Fine-tuning |
| **2** | **Transient noise** | React hooks v18, Next.js App Router, specific framework syntax |

From that classification, we prescribe **stable, long-term learning pathways** that won't go obsolete. We're enabling the **Forever Talent ecosystem** — careers built on skills that matter.

Built by **Altruva Lab** and deployed through **LAEM Institute** to serve emerging markets first.

---

## 📦 What This Repo Contains

This repository contains the **complete AdaRSS platform**:

- ✅ **DistilBERT fine-tuned model** – classifies skills as Enduring / Emergent / Transient
- ✅ **Sentence‑Transformer similarity** – personalized career advice based on user history
- ✅ **FastAPI backend** – JWT authentication, PostgreSQL, rate limiting, usage tracking
- ✅ **React + TypeScript frontend** – Admin dashboard + client portal
- ✅ **B2B-ready** – Plans, API keys, client management, and usage monitoring
- ✅ **Docker-ready** – simple deployment to any cloud

---

## 🧠 How It Works

### The Classification Model

Input: `"Data Engineer: Apache Spark"`

Output: `Emergent (label: 1)`  
Reasoning: *Currently dominant in big data, but competing frameworks emerging.*

### The Personalization Engine

The system uses Sentence‑Transformer embeddings to compute semantic similarity between a user's work history and a target skill. Based on the similarity score, it delivers one of three types of advice:

| Advice Type | Description |
|-------------|-------------|
| **Continuous Upscaling** | Your background aligns perfectly – deepen your expertise. |
| **Career Broadening** | Your skills transfer well – leverage your experience to pivot. |
| **Change of Profession** | Significant pivot – plan for 18-36 months of dedicated learning. |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         React + TypeScript UI                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │
│  │   Admin     │  │   Client    │  │       Login / Auth           │ │
│  │  Dashboard  │  │  Dashboard  │  │                             │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ JWT + API Keys
┌──────────────────────────────▼──────────────────────────────────────┐
│                          FastAPI Backend                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐  │
│  │   Auth    │ │  Plans &  │ │   API     │ │   Usage / Billing │  │
│  │  (JWT)    │ │  Clients  │ │   Keys    │ │    Tracking       │  │
│  └───────────┘ └───────────┘ └───────────┘ └───────────────────┘  │
│  ┌───────────┐ ┌───────────────────────────────────────────────┐  │
│  │ Classify  │ │         Personalization Engine               │  │
│  │ (DistilBERT)│ │    (Sentence‑Transformer Similarity)        │  │
│  └───────────┘ └───────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                        PostgreSQL                                   │
│  ┌───────┐ ┌───────┐ ┌─────────┐ ┌───────────┐ ┌─────────────────┐│
│  │ Users │ │ Plans │ │ APIKeys │ │ UsageLogs │ │   Subscriptions ││
│  └───────┘ └───────┘ └─────────┘ └───────────┘ └─────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (pnpm preferred)
- PostgreSQL 14+
- (Optional) Docker

### 1. Clone the Repository

```bash
git clone https://github.com/Altruva-Lab/adarss.git
cd adarss
```

### 2. Backend Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL
# Create a database named 'adarss'
# Update DATABASE_URL in .env file

# Seed the admin user and plans (auto-runs on first start)
python -c "import asyncio; from api.main import bootstrap_defaults; asyncio.run(bootstrap_defaults())"

# Start the backend
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup

```bash
cd adarss-ui

# Install dependencies (using pnpm)
pnpm install

# Start the development server
pnpm run dev
```

### 4. Login

- **Admin:** `...` / `...`
- **Clients:** Created by admin via the Admin Dashboard

---

## 📁 Project Structure

```
adarss/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app – endpoints & models
│   ├── database.py          # SQLAlchemy async models (Users, Plans, APIKeys, UsageLogs)
│   ├── dependencies.py      # JWT auth, API key verification, admin checks
│   ├── models.py            # Pydantic schemas
│   ├── config.py            # Environment configuration
│   └── model/
│       └── adarss-distilbert/   # Fine‑tuned DistilBERT model
├── adarss-ui/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # AdminUsers, AdminKeys, Dashboard, Login, Navbar
│   │   ├── context/         # AuthContext (JWT)
│   │   ├── services/        # API client with interceptors
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # Routing
│   │   └── index.css        # Global styles
│   ├── package.json
│   └── ...
├── data/
│   └── sample_annotated.csv # Training dataset (876 samples)
├── brain.py                 # Model training script
├── generate_data.py         # Synthetic data generator
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔑 Business Model

AdaRSS is built as a **B2B platform** with a clear subscription model:

| Plan | Monthly Requests | Price |
|------|------------------|-------|
| **Starter** | 5,000 | Free |
| **Pro** | 50,000 | $49/month |
| **Enterprise** | 500,000 | $199/month |

**Admin capabilities:**
- Create client accounts
- Assign/upgrade/downgrade plans
- Monitor usage across all clients
- Generate and revoke API keys for any client

**Client capabilities:**
- Generate/revoke their own API keys
- View usage stats and plan progress
- Monitor key usage (total requests per key)

---

## 🛠️ Technical Stack

| Layer | Technology |
|-------|------------|
| **AI Model** | DistilBERT (fine‑tuned) + Sentence‑Transformer |
| **Backend** | FastAPI (Python), SQLAlchemy (async) |
| **Database** | PostgreSQL + asyncpg |
| **Authentication** | JWT + bcrypt/passlib |
| **Frontend** | React + TypeScript, Vite |
| **Styling** | Vanilla CSS (no Tailwind) |
| **Deployment** | Docker + Uvicorn |

---

## 📊 API Reference

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/token` | POST | Login with email/password → returns JWT |

### Classification & Advice (JWT required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/classify` | POST | `{ job_title, skill }` → `{ classification, label }` |
| `/advice` | POST | `{ history, target_skill }` → personalized advice |
| `/me` | GET | Get current user profile + plan + usage |

### API Key Management (JWT required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-keys` | GET | List user's API keys with usage counts |
| `/api-keys` | POST | `{ name }` → generate new API key |
| `/api-keys/{key_id}` | DELETE | Revoke an API key |
| `/api-keys/{key_id}/usage` | GET | Usage logs for a specific key |

### Admin Endpoints (JWT + admin role)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/users` | GET | List all users |
| `/admin/users` | POST | Create a new client |
| `/admin/users/{id}/toggle` | PATCH | Activate/deactivate a user |
| `/admin/users/{id}/plan` | POST | Assign/change a user's plan |
| `/admin/keys` | GET | List all API keys with owner info |
| `/admin/generate-key` | POST | Generate key for a specific user |

### Public Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/plans` | GET | List available subscription plans |
| `/` | GET | Health check / welcome message |

---

## 🔐 Security & Rate Limiting

- **JWT tokens** – expire after 30 minutes (configurable)
- **API keys** – use `X-API-Key` header for programmatic access
- **Rate limiting** – 100 requests per minute per API key (configurable)
- **Monthly quotas** – enforced per user based on their plan
- **Password hashing** – bcrypt with work factor 12
- **CORS** – configurable via `ALLOWED_ORIGINS` env var

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t adarss-api .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:pass@host/adarss" \
  -e SECRET_KEY="your-secret-key" \
  adarss-api
```

---

## 📈 Roadmap

### Phase 1: Prototype ✅ (Current)
- DistilBERT fine‑tuned on 876 synthetic samples
- B2B admin + client portals
- API key management with usage tracking
- Subscription plans (Starter/Pro/Enterprise)

### Phase 2: Scale (with seed funding)
- 50,000+ real job postings (scraped from LinkedIn, Indeed)
- Retrain on real data for higher accuracy
- Multi‑label classification (skills can be multiple types)
- Stripe integration for self‑service subscriptions

### Phase 3: Deploy (with Series A)
- Integration with LAEM Institute learning platform (Talented)
- Personalized upskilling recommendations
- Global job market analytics
- Open data releases for research

---

## 📚 Related Projects

- [ATLAS AI](https://github.com/Altruva-Group/ATLAS-AI) – open‑source model teaching AI's causal evolution
- [Lineage](https://github.com/Altruva-Lab/lineage) – structured curriculum of AI's intellectual lineage
- [LAEM Institute](https://www.linkedin.com/company/laem-institute/) – workforce development across Africa
- [Concourx](https://concourx.netlify.app) – social network for professionals

---

## 👤 Author

**Altruva Lab**
**Abdulhakeem Muhammed**  

- GitHub: [altruva-lab](https://github.com/orgs/Altruva-Lab/)
- GitHub: [abdulhakeem-muhammed](https://github.com/ennas-de)
- LinkedIn: [altruva-lab](https://www.linkedin.com/company/altruva-lab)
- LinkedIn: [abdulhakeem-muhammed-ibiyemi](https://www.linkedin.com/in/abdulhakeem-muhammed-ibiyemi/)

---

## 📝 License

Business Source License.

---

## 🙏 Acknowledgments

- My brother, for asking the question that sparked this
- Altruva Lab team for believing in the vision
- LAEM Institute for the deployment partnership
- Open‑source community for Transformers, PyTorch, FastAPI, and React

---

**Last updated:** June 2026  
**Status:** Production‑ready MVP, actively maintained  
**Next phase:** Investment round for scaling

---
