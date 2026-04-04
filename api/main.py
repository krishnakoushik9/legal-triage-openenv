import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.env import LegalEnv
from app.models import Action
from typing import Dict, Any

REQUIRED_ENV_VARS = ["HF_TOKEN"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logging.warning(f"Environment variable {var} not set")

app = FastAPI(title="Legal Triage OpenEnv API")
env = LegalEnv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10240:
        return JSONResponse({"error": "Request too large"}, status_code=413)
    return await call_next(request)

@app.get("/")
def read_root():
    return {"message": "Legal Triage OpenEnv is running"}

@app.get("/health")
def health():
    return {"status": "ok", "environment": "legal-triage-openenv"}

@app.get("/reset")
def reset(task_id: str = None):
    try:
        obs = env.reset(task_id=task_id)
        return obs.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.post("/step")
def step(action: Dict[str, Any]):
    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.get("/state")
def get_state():
    """Returns the current environment state without advancing the episode."""
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal environment error")
