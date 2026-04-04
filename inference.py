import os
<<<<<<< HEAD
import json
import sys
from openai import OpenAI
from app.env import LegalEnv

# Configuration from environment variables ONLY
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

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

def run_inference():
    env = LegalEnv()
    tasks = ["easy", "medium", "hard"]
    MAX_STEPS = 8
    
    for task_name in tasks:
        task_id = f"{task_name}_task"
        try:
            obs = env.reset(task_id=task_id)
            done = False
            rewards_list = []
            
            # Print start line
            print(f"[START] task={task_name} env=legal_triage model={MODEL_NAME}")
            
            for step_n in range(1, MAX_STEPS + 1):
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Observation: {obs.json()}"}
                ]
                
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    
                    res_content = json.loads(response.choices[0].message.content)
                    action_dict = res_content.get("action", {})
                    
                    if not action_dict or 'action_type' not in action_dict or 'content' not in action_dict:
                        action_dict = {"action_type": "draft_response", "content": "Fallback action due to invalid output format"}

                except Exception as e:
                    action_dict = {"action_type": "draft_response", "content": "Fallback action due to LLM error"}

                action_str = json.dumps(action_dict).replace('"', '\\"')
                
                try:
                    obs, reward, done, info = env.step(action_dict)
                    error_msg = "null"
                except Exception as e:
                    reward = 0.0
                    done = True
                    error_msg = str(e)
                    info = {"score": 0.0}
                    
                rewards_list.append(reward)
                done_str = "true" if done else "false"
                
                print(f"[STEP] step={step_n} action={action_str} reward={reward:.2f} done={done_str} error={error_msg}")
                
                if done:
                    break
                    
            success = "true" if info.get("score", 0.0) > 0.0 else "false"
            score = info.get("score", 0.0)
            steps_taken = len(rewards_list)
            rewards_str = ",".join(f"{r:.2f}" for r in rewards_list)
            
            print(f"[END] success={success} steps={steps_taken} score={score:.2f} rewards={rewards_str}")
            
        except Exception as e:
            print(f"[START] task={task_name} env=legal_triage model={MODEL_NAME}")
            print(f"[END] success=false steps=0 score=0.00 rewards= error={str(e)}")

    print("All tasks complete", file=sys.stderr)

if __name__ == "__main__":
    run_inference()
=======
import sys
import json
import requests
from openai import OpenAI

# 1. Exact env var patterns
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
SPACE_URL = os.getenv("SPACE_URL", "http://localhost:7860")

# 2. OpenAI client
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

MAX_STEPS = 8
TASKS = ["legal_classification", "legal_retrieval", "legal_resolution"]

def run_episode(task_name):
    # 5. [START] line
    print(f"[START] task={task_name} env=legal_triage model={MODEL_NAME}", flush=True)
    
    rewards = []
    steps_taken = 0
    score = 0.0
    
    try:
        # 3. Connect via HTTP - Reset
        resp = requests.post(f"{SPACE_URL}/reset", json={"task_id": task_name})
        resp.raise_for_status()
        observation = resp.json()
        
        for step_idx in range(1, MAX_STEPS + 1):
            steps_taken = step_idx
            
            try:
                # 9. Prompt LLM
                prompt = f"Legal Task: {task_name}\nCurrent Observation: {json.dumps(observation)}\n\nPlease provide a structured legal response."
                
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                llm_response = (completion.choices[0].message.content or "").strip()
                
                # 9. Send action to /step
                action = {"action_type": "final_answer", "content": llm_response}
                step_resp = requests.post(f"{SPACE_URL}/step", json=action)
                step_resp.raise_for_status()
                step_data = step_resp.json()
                
                observation = step_data["observation"]
                reward = step_data.get("reward", 0.0)
                done = step_data.get("done", False)
                
                rewards.append(reward)
                score = reward # 10. Score = final reward from the last step
                
                # 5 & 6. [STEP] formatting
                done_str = "true" if done else "false"
                # Replace newlines in action for log single-line consistency
                action_clean = llm_response.replace("\n", " ").replace("\r", "")
                
                print(f"[STEP] step={step_idx} action={action_clean} reward={reward:.2f} done={done_str} error=null", flush=True)
                
                if done:
                    break
            except Exception as e:
                # Error in this specific step
                error_msg = str(e).replace("\n", " ")
                print(f"[STEP] step={step_idx} action=error reward=0.00 done=true error={error_msg}", flush=True)
                break 
                
    except Exception as e:
        # This handles reset failure or other major issues
        error_msg = str(e).replace("\n", " ")
        print(f"Episode Error: {error_msg}", file=sys.stderr)
    finally:
        # 10. Success criteria
        success = score >= 0.1
        success_str = "true" if success else "false"
        
        # 6. [END] formatting
        rewards_formatted = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={success_str} steps={steps_taken} score={score:.3f} rewards={rewards_formatted}", flush=True)

def main():
    # 4. Run ALL 3 tasks sequentially
    for task_name in TASKS:
        run_episode(task_name)

if __name__ == "__main__":
    main()
>>>>>>> 91f159c (Fix POST /reset, Dockerfile, openenv.yaml, inference.py for validator)
