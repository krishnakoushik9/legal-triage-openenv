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

## 🔍 Hackathon Audit — 4th April 2026

### ✅ What Is Built & Working
- **Environment Skeleton:** `app/env.py` contains `LegalEnv` with basic `reset()` and `step()` functions returning observation, reward, done, info.
- **Data Models:** `app/models.py` uses correct Pydantic typing for `Observation`, `Action`, and `RewardInfo`.
- **Reward Shaping:** `app/reward.py` implements dense rewards logic evaluating step actions (+0.2/-0.1 points).
- **Task Variety:** `app/tasks/__init__.py` has exactly 3 tasks (easy, medium, hard).
- **Docker Setup:** `Dockerfile` is clean and correctly exposes port 7860 for FastAPI.

### ❌ What Is Broken / Incomplete
- **Missing `/state` Endpoint:** `api/main.py` only implements `/reset` and `/step`. The OpenEnv specification generally requires `GET /state`.
- **Superficial Knowledge Base:** `app/tasks/__init__.py` uses hardcoded, 1-2 sentence string arrays for knowledge bases. This destroys real-world utility.
- **Brittle Grader Logic:** `app/graders/legal_grader.py` uses basic `in` substring matching for grading (e.g. `any(step.lower() in c for c in contents)`).
- **Non-Compliant Inference Logging:** `inference.py` prints custom text (`--- Starting Task...`) instead of the strictly required `[START]`, `[STEP]`, and `[END]` formats.

### 🚨 Disqualification Risks
- **RED:** `inference.py` fails to emit strictly formatted `[START]`, `[STEP]`, `[END]` logs. This will cause automated evals to parse 0 steps.
- **RED:** `api/main.py` is missing the `GET /state` endpoint, typically required for API-based OpenEnv submissions.
- **AMBER:** The HF Space deploy is UNKNOWN (not deployed yet). If it crashes on start, it is an instant DQ.

### 📊 Current Estimated Score
| Criterion | Max | Now | Gap |
|-----------|-----|-----|-----|
| Real-world utility | 30 | 10 | 20 |
| Task & grader quality | 25 | 15 | 10 |
| Environment design | 20 | 18 | 2 |
| Code quality & spec | 15 | 8 | 7 |
| Creativity & novelty | 10 | 6 | 4 |
| **TOTAL** | **100** | **57** | **43** |

### 🛠️ Fix Priority Queue

**PRIORITY CRITICAL**
FILE: `inference.py` (lines 40-70)
PROBLEM: Missing exact `[START]`, `[STEP]`, `[END]` logs required by the spec.
FIX: Replace custom print statements with the required log formats: `print(f"[START] task={task_id} env=legal-triage-env model={MODEL_NAME}")`, `print(f"[STEP] step={env.current_step} action={action_dict["action_type"]} reward={reward:.2f} done={done} error=null")`, `print(f"[END] success={info.get("score", 0) > 0.5} steps={env.current_step} score={info.get("score", 0):.2f} rewards=...")`.
EFFORT: 15min
BLOCKS: Disqualification / Spec Compliance

**PRIORITY CRITICAL**
FILE: `api/main.py` (line 15)
PROBLEM: Missing `GET /state` endpoint which is required for OpenEnv API compliance.
FIX: Add `@app.get("/state") def state(): return env._get_observation().dict()`
EFFORT: 15min
BLOCKS: Disqualification / Spec Compliance

**PRIORITY HIGH**
FILE: `app/tasks/__init__.py` (lines 5-30)
PROBLEM: The knowledge base and tasks are extremely superficial (hardcoded short strings), limiting real-world utility.
FIX: Expand the knowledge base to include actual legal texts or mock statutes, and make the queries more complex.
EFFORT: 1hr
BLOCKS: Real-world utility (30 pts)

**PRIORITY MEDIUM**
FILE: `app/graders/legal_grader.py` (lines 14-41)
PROBLEM: Grader uses simple substring matching (`any(step.lower() in c for c in contents)`), making it easily spoofable or brittle.
FIX: Implement a more robust grading logic, potentially using an LLM-as-a-judge or exact keyword combinations with regex.
EFFORT: 1hr
BLOCKS: Task & grader quality (25 pts)

### 🏁 Win Conditions
What the project needs to score 85+/100 and pass all automated gates:
1. **Fix inference.py instantly:** Ensure the `[START]`, `[STEP]`, `[END]` logs match the parsing regex perfectly.
2. **Implement `/state` endpoint:** Ensure the API is fully spec-compliant.
3. **Deepen the Domain:** Replace the 3-line string arrays in `tasks/__init__.py` with realistic legal case files or JSON dumps of mock laws to recover ~15 points in Real-World Utility.
4. **Harden the Grader:** Ensure `legal_grader.py` cannot be tricked by an agent just vomiting keywords.
