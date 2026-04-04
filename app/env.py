import numpy as np
from typing import List, Dict, Any, Tuple
from app.models import Observation, Action
from app.tasks import get_task
from app.reward import RewardShaper
from app.graders.legal_grader import LegalGrader

class LegalEnv:
    def __init__(self):
        self.difficulties = ["easy", "medium", "hard"]
        self.current_diff_idx = 0
        self.reward_shaper = RewardShaper()
        self.grader = LegalGrader()
        self.max_steps = 8
        self.total_reward_so_far = 0.0
        self.reset()

    def reset(self, task_id: str = None) -> Observation:
        if task_id and task_id.split('_')[0] in self.difficulties:
            difficulty = task_id.split('_')[0]
        else:
            difficulty = self.difficulties[self.current_diff_idx]
            self.current_diff_idx = (self.current_diff_idx + 1) % len(self.difficulties)
            
        self.task = get_task(difficulty)
        self.history: List[Action] = []
        self.current_step = 0
        self.done = False
        self.total_reward_so_far = 0.0
        
        return self._get_observation()

    def step(self, action_dict: Dict[str, Any]) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self.done:
            raise Exception("Environment already done. Call reset().")
            
        action = Action(**action_dict)
        reward = self.reward_shaper.calculate_reward(action, self.task, self.history)
        
        self.total_reward_so_far += reward
        self.total_reward_so_far = max(0.0, min(1.0, self.total_reward_so_far))
        
        self.history.append(action)
        self.current_step += 1
        
        if action.action_type == "final_answer" or self.current_step >= self.max_steps:
            self.done = True
            
        info = {}
        if self.done:
            info["score"] = self.grader.grade(self.task, self.history)
            
        return self._get_observation(), reward, self.done, info

    def state(self) -> Dict[str, Any]:
        return {
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "task_name": self.task["id"] if hasattr(self, 'task') else "",
            "current_observation": self._get_observation().dict(),
            "episode_done": self.done,
            "total_reward_so_far": self.total_reward_so_far
        }

    def _get_observation(self) -> Observation:
        context = []
        if any(a.action_type == "retrieve_doc" for a in self.history):
            context = self.task["knowledge_base"]
            
        return Observation(
            user_query=self.task["query"],
            context_documents=context,
            current_step=self.current_step,
            history=[f"{a.action_type}: {a.content}" for a in self.history]
        )
