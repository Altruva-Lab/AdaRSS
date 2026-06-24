# AdaRSS: Adaptive Representation Systems for Structured Skilled Data

> *End skill instability. Build careers that last.*

### Building the World's Career Stability Intelligence Layer

AdaRSS is a workforce intelligence platform that helps individuals, institutions, and governments identify which skills create durable careers in a rapidly changing economy.

As technology evolves, workers increasingly invest years learning tools, frameworks, and platforms that may become obsolete within a short period of time. Educational institutions struggle to keep curricula aligned with industry needs, while employers face growing uncertainty around workforce preparedness.

AdaRSS addresses this challenge by classifying skills according to their long-term stability and relevance, helping people and organizations make better decisions about learning, workforce development, and talent investment.

---

## 🌍 The Problem

The modern workforce faces an unprecedented challenge:

* Technologies evolve faster than educational systems.
* Workers frequently invest years mastering unstable skills.
* Training institutions struggle to identify lasting competencies.
* Employers face widening gaps between talent supply and workforce demand.
* Emerging economies bear a disproportionate share of these challenges.

The result is workforce instability, wasted educational investment, and reduced economic mobility.

---

## 💡 Our Solution

AdaRSS provides intelligence for identifying durable, transferable, and future-relevant skills.

Using artificial intelligence and workforce intelligence methodologies, AdaRSS analyzes skills and classifies them into three categories:

| Label | Category             | Description                                                            |
| ----- | -------------------- | ---------------------------------------------------------------------- |
| **0** | Enduring Foundations | Skills that remain valuable across industries and technological shifts |
| **1** | Emergent Necessities | Skills experiencing strong growth and increasing market demand         |
| **2** | Transient Skills     | Skills tied to temporary technologies, frameworks, or trends           |

This enables individuals, educational institutions, workforce agencies, and governments to make informed decisions about skill development and talent strategy.

---

## 🎯 Who AdaRSS Serves

### Individuals

Build careers on durable skills instead of temporary trends.

### Educational Institutions

Design curricula around long-term workforce needs.

### Workforce Development Agencies

Improve employability outcomes through evidence-based skill planning.

### Governments

Strengthen workforce resilience and economic competitiveness.

### Employers

Understand the stability and transferability of workforce capabilities.

---

## 📸 Product Screenshots

### Skill Classification Engine

![Skill Classification](./docs/screenshots/skill-classification.png)



---

### Personalized Career Guidance

![Career Guidance](./docs/screenshots/career-guidance.png)



---

### Administrative Dashboard

![Admin Dashboard](./docs/screenshots/admin-dashboard.png)



---

### Client Dashboard

![Client Dashboard](./docs/screenshots/client-dashboard.png)



---

### API Usage & Analytics

![Usage Analytics](./docs/screenshots/usage-analytics.png)



---

## 📈 Why It Matters

The future of work requires more than identifying today's popular skills.

It requires understanding:

* Which skills remain valuable over decades.
* Which skills are emerging as critical workforce capabilities.
* Which skills are likely to become obsolete.
* How workers can build resilient career pathways.

AdaRSS exists to provide that intelligence layer.

Our long-term vision is to become the global infrastructure for workforce stability and career resilience.


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

## 🌱 Expected Impact

- Reduce workforce instability
- Improve educational alignment
- Increase employability outcomes
- Support workforce planning
- Strengthen economic mobility


## 🤝 Partnerships & Funding

AdaRSS is currently seeking:

- Pilot institutions
- Workforce development partners
- Research collaborators
- Grant funding
- Strategic investors

To discuss collaboration, contact:
dev.abdulhakeem@gmail.com

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
