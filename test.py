from app.env import LegalEnv
import json

def run_tests():
    env = LegalEnv()
    tasks = ["easy_classification", "medium_retrieval", "hard_resolution"]
    results = {}

    for task_id in tasks:
        print(f"Testing task: {task_id}")
        obs = env.reset(task_id=task_id)
        done = False
        total_reward = 0
        
        # Simple heuristic agent for testing
        while not done:
            task = env.task
            step = env.current_step
            
            if step == 0:
                action = {"action_type": "classify", "content": task["expected_classification"]}
            elif step == 1:
                action = {"action_type": "retrieve_doc", "content": "Looking for legal context"}
            elif step == 2:
                action = {"action_type": "draft_response", "content": "Drafting advice based on documents"}
            else:
                action = {"action_type": "final_answer", "content": "Here is the final resolution."}
                
            obs, reward, done, info = env.step(action)
            total_reward += reward
            print(f"  Step {step}: Reward {reward:.2f}")

        results[task_id] = {
            "total_reward": total_reward,
            "score": info.get("score", 0),
            "steps": env.current_step
        }
        print(f"Task {task_id} completed. Score: {info.get('score', 0)}")

    print("\n--- Test Results ---")
    print(json.dumps(results, indent=2))
    
    # Calculate failure rate (score < 0.5 is considered failure for this test)
    failures = sum(1 for r in results.values() if r["score"] < 0.5)
    print(f"Failure Rate: {failures}/{len(tasks)}")

if __name__ == "__main__":
    run_tests()
