# Open Source Bottleneck Detector

> An evidence-based bottleneck detector for open source contributors — powered by real GitHub data, not LLM guesses.

Built for the **WeMakeDevs × Cognee AI Hackathon** by **Saumyadeep Mishra**.

---

## The Problem

Many open source contributors struggle to identify why they are not progressing. Most AI tools just ask an LLM to guess the bottleneck — which leads to generic, hallucinated advice that doesn't reflect reality.

## The Solution

This system detects bottlenecks using **evidence**, not opinion.

Instead of:
```
User → LLM → Advice
```

We do:
```
User Data + GitHub Evidence + Evidence Scoring + Bottleneck Ranking → LLM Explanation
```

The LLM explains bottlenecks. It does NOT decide them. Evidence does.

---

## How It Works

1. User submits a message describing their skills, weaknesses, and goals
2. System stores the raw message and extracts structured memories (skills, weaknesses)
3. User registers their GitHub username
4. On analysis, the system fetches real GitHub activity and combines it with stored memories
5. Evidence objects are generated and scored from both sources
6. Bottlenecks are ranked by severity based on evidence
7. LLM generates a human-readable explanation with actionable steps
8. Final report is saved and retrievable

---

## Tech Stack

- **Backend** — Python, FastAPI
- **Database** — SQLite
- **Memory Layer** — Custom extraction (Cognee integration in progress)
- **AI Layer** — Groq (LLaMA via OpenAI-compatible API)
- **External Data** — GitHub Public API

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Submit a message, extract and store memories |
| `POST` | `/register` | Register a GitHub username for a user |
| `POST` | `/analyze` | Run full evidence-based bottleneck analysis |
| `GET` | `/report/{id}` | Retrieve a saved report |

---

## Project Structure

```
app/
├── main.py
├── api/
│   ├── chat.py
│   ├── analyze.py
│   ├── register.py
│   └── report.py
├── services/
│   ├── message_service.py
│   ├── memory_service.py
│   ├── github_service.py
│   ├── evidence_service.py
│   ├── bottleneck_service.py
│   ├── analysis_service.py
│   ├── report_service.py
│   └── llm_service.py
├── models/
│   └── schemas.py
└── database/
    └── db.py
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SdmWorks7/open-source-bottleneck-detector
cd open-source-bottleneck-detector
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn aiosqlite httpx groq python-dotenv
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

### 6. Open the interactive docs

```
http://127.0.0.1:8000/docs
```

---

## Example Flow

**Step 1 — Submit a message**
```json
POST /chat
{
  "user_id": 1,
  "message": "I know Java but struggle with Git."
}
```

**Step 2 — Register GitHub username**
```json
POST /register
{
  "user_id": 1,
  "github_username": "your_github_username"
}
```

**Step 3 — Run analysis**
```json
POST /analyze
{
  "user_id": 1
}
```

**Step 4 — Retrieve report**
```
GET /report/{report_id}
```

---

## Author

**Saumyadeep Mishra**
