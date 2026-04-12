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

@app.post("/reset")
def reset(request: Optional[ResetRequest] = None, task_id: Optional[str] = None):
    try:
        t_id = task_id or (request.task_id if request else None)
        obs = env.reset(task_id=t_id)
        return obs.dict()
    except Exception as e:
        logging.error(f"Error in /reset: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.post("/step")
def step(action: Dict[str, Any]):
    try:
        # Action model handles validation
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        logging.error(f"Error in /step: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.get("/state")
def get_state():
    """Returns the current environment observation without advancing the episode."""
    try:
        return env._get_observation().dict()
    except Exception as e:
        logging.error(f"Error in /state: {e}")
        raise HTTPException(status_code=500, detail="Internal environment error")
