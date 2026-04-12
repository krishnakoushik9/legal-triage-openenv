import os
import logging
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.env import LegalEnv
from app.models import Action
from typing import Dict, Any
from openai import OpenAI

REQUIRED_ENV_VARS = ["HF_TOKEN"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logging.warning(f"Environment variable {var} not set")

app = FastAPI(title="Legal Triage OpenEnv API")
env = LegalEnv()

SYSTEM_PROMPT = """
You are a legal reasoning agent.
Your goal is to solve the user's legal issue step-by-step using the provided environment.

Available Actions:
- classify: Categorize the query (e.g., civil_dispute, criminal, contract, tort, IP, employment, privacy, corporate, family).
- retrieve_doc: Get relevant legal snippets from the knowledge base.
- draft_response: Prepare a draft of the legal advice.
- escalate: Use for complex cases that need higher authority (primarily for hard tasks).
- final_answer: Provide the final structured resolution to the user.

Rules:
- Think step-by-step.
- Use one action at a time.
- If you use 'retrieve_doc', the next observation will contain relevant legal documents.
- Always conclude with 'final_answer'.
- Maximize your reward by being accurate and following the legal process.

You must output your next action in the following JSON format:
{
  "thought": "Your reasoning here",
  "action": {
    "action_type": "one of the available actions",
    "content": "the content for the action"
  }
}
"""

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

@app.get("/health")
def health():
    return {"status": "ok", "environment": "legal-triage-openenv"}

@app.post("/reset")
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
    """Returns the current environment state (observation) without advancing the episode."""
    try:
        return env._get_observation().dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal environment error")

@app.post("/token")
async def set_token(data: Dict[str, str]):
    token = data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token required")
    os.environ["HF_TOKEN"] = token
    return {"message": "Token set successfully"}

@app.post("/auto-step")
async def auto_step():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise HTTPException(status_code=400, detail="HF_TOKEN not set. Use /token or set env var.")
    
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=token
        )
        
        obs = env._get_observation()
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Observation: {obs.json()}"}
        ]
        
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        res_content = json.loads(response.choices[0].message.content)
        action_dict = res_content.get("action", {})
        
        if not action_dict or 'action_type' not in action_dict or 'content' not in action_dict:
             raise HTTPException(status_code=500, detail="Model returned invalid action format")

        obs, reward, done, info = env.step(action_dict)
        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        logging.error(f"Auto-step error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend from root - MUST BE LAST
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")

app.mount("/", StaticFiles(directory="frontend"), name="frontend")
