# AI Resume Analyzer & Job Description Matching System

A full-stack web application that parses resumes, generates an explainable
ATS score, matches resumes against job descriptions, and produces
AI-assisted improvement suggestions.

## Modules

1. **Resume Parsing** — extracts name, email, phone, education, experience,
   skills, projects, and certifications from PDF/DOCX resumes.
2. **ATS Resume Analysis** — rule-based, explainable scoring engine
   (Formatting 15, Skills 20, Projects 20, Experience 20, Education 10,
   Grammar/Keywords 15).
3. **Job Description Matching** — compares resume skills against JD
   required skills using keyword matching + semantic similarity
   (sentence-transformers, with a TF-IDF fallback if offline).
4. **AI Career Coach** — uses an LLM (OpenAI/Gemini, pluggable) purely for
   feedback, summaries, and improvement suggestions. Skill extraction is
   NEVER done via AI — only rule-based NLP.

## Tech Stack

**Frontend:** React.js, Tailwind CSS v4, Shadcn-style UI, React Router, Axios, Recharts
**Backend:** FastAPI, Uvicorn, SQLAlchemy, Pydantic
**Parsing:** pdfplumber, PyMuPDF, python-docx
**NLP:** spaCy, sentence-transformers, scikit-learn (TF-IDF fallback)
**Database:** SQLite (dev) → PostgreSQL (swap via `DATABASE_URL`)
**Auth:** JWT (Admin / Recruiter roles)

## Project Structure

```
AI-Resume-Analyzer/
├── frontend/               React app (Vite)
│   └── src/
│       ├── components/     UI primitives, layout, feature components
│       ├── pages/          Login, Register, Dashboard, Upload*, History, Analysis
│       ├── context/        AuthContext
│       └── services/       Axios API clients (one per backend resource)
├── backend/                FastAPI app
│   └── app/
│       ├── api/            Route handlers
│       ├── models/         SQLAlchemy models
│       ├── schemas/        Pydantic request/response schemas
│       ├── services/       Business logic layer
│       ├── ats/            ATS scoring engine (6 category scorers)
│       ├── parser/         Resume text extraction + field parsing
│       ├── matcher/        Keyword + semantic matching engine
│       ├── ai/             AI suggestion providers (mock/OpenAI/Gemini)
│       ├── utils/          Security, JWT, file handling
│       └── core/           Config, DB session, seed scripts
├── uploads/                 Uploaded resume files (gitignored)
├── database/                SQLite file lives here (gitignored)
└── PROGRESS.md              Module-by-module build log
```

## Quick Start

You'll need two terminals — one for the backend, one for the frontend.

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm   # optional, improves name extraction

cp .env.example .env              # defaults work out of the box (SQLite + mock AI)

python -m app.core.init_db        # creates all tables
python -m app.core.seed_skills    # seeds the master skills list

uvicorn app.main:app --reload     # runs on http://localhost:8000
```

API docs (Swagger UI): **http://localhost:8000/docs**

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env              # points at http://localhost:8000/api by default
npm run dev                       # runs on http://localhost:5173
```

Open **http://localhost:5173**, register an account, and you're in.

## Configuration Notes

- **Database**: SQLite by default (`backend/database/app.db`). To switch to
  Postgres, set `DATABASE_URL=postgresql://user:pass@host:5432/dbname` in
  `backend/.env` — no code changes needed.
- **AI Suggestions**: runs in `mock` mode by default (no API key needed —
  the app is fully functional without one). To use real AI feedback, set in
  `backend/.env`:
  ```
  AI_PROVIDER=openai        # or "gemini"
  OPENAI_API_KEY=sk-...
  ```
  If the real provider ever fails (bad key, rate limit, network issue), the
  app automatically falls back to the mock provider rather than breaking.
- **Semantic matching**: `sentence-transformers` downloads its model
  (~90MB) from Hugging Face on first use. If unavailable, matching
  automatically falls back to TF-IDF cosine similarity — still fully
  functional, just less nuanced on wording differences.

## Roles

- **Recruiter**: can upload/view/analyze only their own resumes and job descriptions.
- **Admin**: sees everything across all recruiters (used for the global dashboard view).

## Build Status

All 12 planned modules are complete — see `PROGRESS.md` for the module-by-module log.

## Known Limitations (documented for your viva)

- Resume section parsing uses heuristics (blank-line-separated entries).
  Resumes that list multiple entries as bare single lines with no blank
  line between them will be treated as one entry rather than several.
- Skill extraction uses a curated ~47-skill controlled vocabulary
  (`backend/app/parser/skill_data.py`) rather than an open-ended list —
  intentional, per the spec's requirement that skill extraction not use AI.
