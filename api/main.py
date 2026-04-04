import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.env import LegalEnv
from app.models import Action
from typing import Dict, Any

REQUIRED_ENV_VARS = ["HF_TOKEN"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logging.warning(f"Environment variable {var} not set")
=======
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.env import LegalEnv
from app.models import Action

# Setup logging
logging.basicConfig(level=logging.INFO)
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)

app = FastAPI(title="Legal Triage OpenEnv API")
env = LegalEnv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

<<<<<<< HEAD
=======
class ResetRequest(BaseModel):
    task_id: Optional[str] = None

>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10240:
        return JSONResponse({"error": "Request too large"}, status_code=413)
    return await call_next(request)

@app.get("/")
<<<<<<< HEAD
def read_root():
    return {"message": "Legal Triage OpenEnv is running"}
=======
def root():
    return {"message": "Legal Triage OpenEnv is running", "status": "ok"}
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)

@app.get("/health")
def health():
    return {"status": "ok", "environment": "legal-triage-openenv"}

@app.post("/reset")
<<<<<<< HEAD
def reset(task_id: str = None):
    try:
        obs = env.reset(task_id=task_id)
        return obs.dict()
    except Exception as e:
=======
def reset(request: Optional[ResetRequest] = None):
    try:
        task_id = request.task_id if request else None
        obs = env.reset(task_id=task_id)
        return obs
    except Exception as e:
        logging.error(f"Error in /reset: {e}")
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.post("/step")
def step(action: Dict[str, Any]):
    try:
        obs, reward, done, info = env.step(action)
        return {
<<<<<<< HEAD
            "observation": obs.dict(),
=======
            "observation": obs,
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
<<<<<<< HEAD
=======
        logging.error(f"Error in /step: {e}")
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.get("/state")
def get_state():
    """Returns the current environment state without advancing the episode."""
    try:
        return env.state()
    except Exception as e:
<<<<<<< HEAD
=======
        logging.error(f"Error in /state: {e}")
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
        raise HTTPException(status_code=500, detail="Internal environment error")
