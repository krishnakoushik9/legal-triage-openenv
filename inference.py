import os
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

# 2. OpenAI client initialized lazily
def get_client():
    if not API_KEY:
        # In some environments, the key might be missing but we still want the script to start
        # and only fail if the actual API call is made.
        print("Warning: HF_TOKEN/API_KEY is missing. API calls will likely fail.", file=sys.stderr)
    return OpenAI(base_url=API_BASE_URL, api_key=API_KEY or "not-set")

MAX_STEPS = 8
TASKS = ["legal_classification", "legal_retrieval", "legal_resolution"]

def run_episode(task_name):
    # 5. [START] line
    print(f"[START] task={task_name} env=legal-triage-openenv model={MODEL_NAME}", flush=True)
    
    rewards = []
    steps_taken = 0
    final_score = 0.0
    client = get_client()
    
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
                action_type = "final_answer"
                action = {"action_type": action_type, "content": llm_response}
                step_resp = requests.post(f"{SPACE_URL}/step", json=action)
                step_resp.raise_for_status()
                step_data = step_resp.json()
                
                observation = step_data["observation"]
                reward = step_data.get("reward", 0.0)
                done = step_data.get("done", False)
                info = step_data.get("info", {})
                
                rewards.append(reward)
                if done:
                    final_score = info.get("score", reward)
                
                # 5 & 6. [STEP] formatting
                done_str = "true" if done else "false"
                
                print(f"[STEP] step={step_idx} action={action_type} reward={reward:.2f} done={done_str} error=null", flush=True)
                
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
        success = final_score >= 0.5
        success_str = "true" if success else "false"
        
        # 6. [END] formatting
        rewards_formatted = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={success_str} steps={steps_taken} score={final_score:.3f} rewards={rewards_formatted}", flush=True)

def main():
    # 4. Run ALL 3 tasks sequentially
    for task_name in TASKS:
        run_episode(task_name)

if __name__ == "__main__":
    main()
