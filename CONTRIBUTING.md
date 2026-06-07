# Contributing to ParthaGPT-AI-OS 🤖

Thank you for your interest in contributing to ParthaGPT-AI-OS!  
This guide will help SSoC Season 5 participants go from zero to their first merged PR.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Code Style](#code-style)
- [Need Help?](#need-help)

---

## Project Overview

ParthaGPT-AI-OS is a **persistent autonomous AI operating platform** — not a simple chatbot. It combines:

- 🧠 **Semantic Memory Engine** — vector-based long-term memory via ChromaDB
- 🪞 **Reflection Engine** — analyzes conversations, goals, and behaviors
- ⚡ **Adaptive Personality Engine** — dynamically adjusts tone and reasoning style
- 🤖 **Multi-Agent Architecture** — Strategist, Coding, Research, Creativity, and Career agents
- ⚙️ **Autonomous Workflow Engine** — intent detection, plan generation, tool chaining
- 🌐 **Web-Aware Intelligence** — live AI trend research and web intelligence

**Tech Stack:** Python · Groq API · RAG Architecture · ChromaDB · Sentence Transformers · Streamlit

---

## Prerequisites

Before setting up, make sure you have:

- Python 3.9 or higher
- `pip` (Python package manager)
- Git
- A free [Groq API key](https://console.groq.com)

---

## Local Setup

```bash
# 1. Fork the repo on GitHub, then clone YOUR fork
git clone https://github.com/YOUR_USERNAME/ParthaGPT-AI-OS.git
cd ParthaGPT-AI-OS

# 2. Add the original repo as upstream (to sync later)
git remote add upstream https://github.com/parthakhare1812/ParthaGPT-AI-OS.git

# 3. Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create your .env file
# Create a file called .env in the root folder and add:
# GROQ_API_KEY=your_api_key_here

# 6. Run memory ingestion first (required before running the app)
python -m backend.ingest

# 7. Launch the AI OS
streamlit run app.py
```

---

## Project Structure

```
ParthaGPT-AI-OS/
│
├── app.py                        # Streamlit entry point — run this to start
│
├── backend/                      # Core AI logic
│   ├── chatbot.py                # Main chat orchestration
│   ├── ingest.py                 # Memory ingestion pipeline
│   ├── retriever.py              # RAG retrieval logic
│   ├── prompts.py                # Prompt templates
│   ├── personality_engine.py     # Adaptive personality system
│   ├── reflection_engine.py      # Self-reflection & cognition reports
│   ├── goal_engine.py            # Goal tracking and analysis
│   ├── task_engine.py            # Task management
│   ├── workflow_engine.py        # Autonomous workflow orchestration
│   ├── memory_manager.py         # Long-term memory management
│   ├── live_ingest.py            # Real-time memory ingestion
│   ├── agents/                   # Multi-agent system (Strategist, Coder, etc.)
│   ├── tools/                    # Agent tools (web search, file ops, etc.)
│   └── background_agents/        # Persistent background cognition agents
│
├── frontend/                     # Streamlit UI components
│   ├── memory_viewer.py          # Memory observability dashboard
│   ├── reflection_viewer.py      # Reflection engine UI
│   ├── workflow_viewer.py        # Workflow dashboard
│   └── agent_monitor.py         # Live agent activity panel
│
├── data/                         # Input data for memory ingestion
├── memory/                       # Persistent memory storage
├── vector_db/                    # ChromaDB vector database files
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview
```

---

## How to Contribute

### Step 1 — Find or Create an Issue
- Check [open issues](../../issues) for anything labeled `good first issue` or `documentation`
- If you spot something missing, open an issue first and describe what you'd like to fix
- Wait for the maintainer to approve before starting work

### Step 2 — Claim the Issue
Comment on the issue:
> "Hi! I'm a SSoC Season 5 participant. I'd like to work on this — could I be assigned?"

### Step 3 — Sync and Branch
```bash
# Always sync with upstream before creating a branch
git fetch upstream
git merge upstream/main

# Create a new branch — never work on main directly
git checkout -b fix/your-issue-description
```

### Step 4 — Make Your Changes
- Work inside the relevant folder (`backend/`, `frontend/`, etc.)
- Test locally with `streamlit run app.py` before pushing
- Never commit your `.env` file or Groq API key

### Step 5 — Push and Open a PR
```bash
git add .
git commit -m "docs: add CONTRIBUTING.md for SSoC contributors (#1)"
git push origin fix/your-issue-description
```

Then open a Pull Request on GitHub — you'll see a yellow banner prompting you.

---

## Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type: short description (#issue-number)
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructuring, no behavior change |
| `test` | Adding or fixing tests |
| `chore` | Maintenance, dependency updates |

**Good examples:**
```
docs: add CONTRIBUTING.md for SSoC contributors (#1)
fix: handle empty Groq API response in chatbot.py (#5)
feat: add web search tool to research agent (#8)
```

**Bad examples:**
```
updated stuff
final fix pls merge
asdfasdf
```

---

## Pull Request Guidelines

Use this PR description template:

```markdown
## What this does
Brief summary of the change.

## Why
Closes #<issue-number>. One line explaining the problem solved.

## Testing
- How did you test this locally?
- e.g., "Ran streamlit run app.py, verified memory viewer loads correctly"

## Screenshots (if UI change)
Add before/after screenshots here.
```

**Rules:**
- One issue = one PR (keep PRs small and focused)
- If changes are requested, just commit on the same branch and push — PR updates automatically
- Be patient and respectful — maintainers are volunteers

---

## Code Style

- Follow [PEP 8](https://pep8.org/) Python style guidelines
- Add docstrings to every function:

```python
def retrieve_context(query: str, top_k: int = 5) -> list:
    """
    Retrieve the top-k most semantically relevant memory chunks.

    Args:
        query (str): The user's input query.
        top_k (int): Number of results to return. Defaults to 5.

    Returns:
        list: A list of relevant memory/document chunks from ChromaDB.
    """
```

- Use clear, descriptive variable names
- Keep functions short — each should do one thing
- **Never** commit `.env` files, API keys, or `vector_db/` contents

---

## Need Help?

- Comment on the relevant GitHub issue with your question
- Tag `@parthakhare1812` politely if you're stuck
- Be specific — describe what you tried and what error you got

We're glad you're here. Happy contributing! 🚀
