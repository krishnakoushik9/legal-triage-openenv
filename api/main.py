import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.env import LegalEnv
from app.models import Action

# Setup logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Legal Triage OpenEnv API")
env = LegalEnv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ResetRequest(BaseModel):
    task_id: Optional[str] = None

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10240:
        return JSONResponse({"error": "Request too large"}, status_code=413)
    return await call_next(request)

@app.get("/")
def root():
    return {"message": "Legal Triage OpenEnv is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok", "environment": "legal-triage-openenv"}

@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    try:
        task_id = request.task_id if request else None
        obs = env.reset(task_id=task_id)
        return obs
    except Exception as e:
        logging.error(f"Error in /reset: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.post("/step")
def step(action: Dict[str, Any]):
    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        logging.error(f"Error in /step: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.get("/state")
def get_state():
    """Returns the current environment state without advancing the episode."""
    try:
        return env._get_observation()
    except Exception as e:
        logging.error(f"Error in /state: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")
