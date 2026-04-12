---
type: project
name: Legal Triage OpenEnv
description: Autonomous legal assistance environment for triage and resolution.
language: Python, TypeScript, HTML, CSS
stack: FastAPI, OpenAI, Pydantic, Docker
status: active
path: /home/krsna/Desktop/meta
github: not found
date-scanned: 2026-04-04
key-files: api/, frontend/, app/, Dockerfile, requirements.txt
tags: [ai, legal-tech, openenv, hackathon, fastapi]
---

# 💻 Legal Triage OpenEnv

## 📋 Overview
An autonomous legal environment for triage and resolution, built for the OpenEnv hackathon. It features 3 task levels: easy (classification), medium (retrieval), and hard (full resolution).

**Path:** `/home/krsna/Desktop/meta`
**Stack:** FastAPI, OpenAI, Docker
**GitHub:** Not found (OpenEnv repository)

## 📁 Project Structure
- `api/main.py`: FastAPI backend interface.
- `frontend/`: TypeScript-powered dashboard for the agent environment.
- `app/`: Core agent logic, reward systems, and task graders.
- `Dockerfile`: Container configuration for deployment.
- `openenv.yaml`: OpenEnv-specific environment settings.

## 📦 Dependencies
- `fastapi`, `uvicorn`, `pydantic`
- `openai`, `numpy`, `python-dotenv`
- `jinja2`

## 🚀 How to Run
Use `pip install -r requirements.txt` then `python test.py` or run the FastAPI app via `uvicorn api.main:app`.

## 🔗 Links
- [Open Folder](file:///home/krsna/Desktop/meta)
- [GitHub](not found)

## 📝 Notes
- Features deterministic grading and dense reward shaping for legal tasks.
- Ready for deployment on Hugging Face (HF) Spaces.

---

🔗 Related

[[Projects/Projects-Index]]
[[🏠 Dashboard]]
[[Goals/Goals-Overview]]

## 🔍 Hackathon Audit — 12th April 2026 (Updated)

### ✅ What Is Built & Working
- **Environment Skeleton:** `app/env.py` contains `LegalEnv` with full `reset()`, `step()`, and `state()` functions.
- **Data Models:** `app/models.py` uses correct Pydantic typing for `Observation`, `Action`, and `RewardInfo`.
- **Reward Shaping:** `app/reward.py` implements delta-score dense rewards with efficiency penalties.
- **Task Variety:** 3 tasks (easy, medium, hard) with deep legal domain knowledge.
- **Docker Setup:** `Dockerfile` is robust with system dependencies and healthchecks.
- **Spec Compliance:** `inference.py` follows strict `[START]`, `[STEP]`, `[END]` logging formats.
- **API Spec:** `api/main.py` implements `/reset`, `/step`, and the required `/state` endpoints with correct observation schemas.

### 🛠️ Fix Status
- **COMPLETED:** `inference.py` log formats.
- **COMPLETED:** `GET /state` endpoint implementation.
- **COMPLETED:** Knowledge base expansion in `app/tasks/__init__.py`.
- **COMPLETED:** Robust rubric-based grading in `app/graders/legal_grader.py`.

### 📊 Updated Estimated Score
| Criterion | Max | Now | Gap |
|-----------|-----|-----|-----|
| Real-world utility | 30 | 28 | 2 |
| Task & grader quality | 25 | 22 | 3 |
| Environment design | 20 | 19 | 1 |
| Code quality & spec | 15 | 15 | 0 |
| Creativity & novelty | 10 | 8 | 2 |
| **TOTAL** | **100** | **92** | **8** |

### 🏁 Win Conditions
Project is now fully spec-compliant and ready for reconsideration.
