import os
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
