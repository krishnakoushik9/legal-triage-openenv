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
        self.hints = [] # New: dynamic hints from actions
        self.precedent_analysis = [] # New: deep dives into precedents
        self.client_interviews = [] # New: insights from client interviews
        self.draft_reviews = [] # New: feedback from partner reviews
        self.billable_hours = 0.0 # New: cost tracking
        
        return self._get_observation()

    def step(self, action_dict: Dict[str, Any]) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        if self.done:
            raise Exception("Environment already done. Call reset().")
            
        action = Action(**action_dict)

        # Agentic logic for specific actions
        if action.action_type == "escalate":
            # Provide a "Senior Counsel" hint based on the task
            case = self.task.get("case_data", {})
            elements = case.get("expected_resolution_elements", [])
            if elements:
                hint = f"Senior Counsel Note: Ensure you focus on {elements[0]} and {elements[-1]} for a strong resolution."
                if hint not in self.hints:
                    self.hints.append(hint)
            else:
                self.hints.append("Senior Counsel Note: Re-read the facts carefully for procedural inconsistencies.")

        elif action.action_type == "analyze_precedent":
            # Deep dive into the precedents mentioned in the task
            case = self.task.get("case_data", {})
            precedents = case.get("prior_precedents", [])
            if precedents:
                for p in precedents:
                    analysis = f"Deep Analysis of {p}: This case confirms the applicability of {case.get('relevant_statutes', ['relevant law'])[0]} in similar fact patterns."
                    if analysis not in self.precedent_analysis:
                        self.precedent_analysis.append(analysis)
            else:
                self.precedent_analysis.append("No specific precedents found for this jurisdiction, applying general common law principles.")

        elif action.action_type == "interview_client":
            case = self.task.get("case_data", {})
            hidden = case.get("hidden_facts", "Client says: I don't have any more documents, but I'm very stressed about the timeline and need this resolved quickly.")
            if hidden not in self.client_interviews:
                self.client_interviews.append(f"Client Interview Transcript: {hidden}")
                
        elif action.action_type == "review_draft":
            drafts = [a.content for a in self.history if a.action_type == "draft_response"]
            if not drafts:
                self.draft_reviews.append("Partner Review: You need to write a draft_response first before I can review it.")
            else:
                last_draft = drafts[-1]
                elements = self.task.get("case_data", {}).get("expected_resolution_elements", [])
                missing = [e for e in elements if e.lower() not in last_draft.lower()]
                if missing:
                    self.draft_reviews.append(f"Partner Review: The draft is missing focus on: {missing[0]}. Please revise.")
                else:
                    self.draft_reviews.append("Partner Review: The draft looks solid. Proceed to final_answer.")

        # Update billable hours
        action_costs = {
            "classify": 0.5,
            "retrieve_doc": 1.0,
            "analyze_precedent": 2.0,
            "interview_client": 1.5,
            "draft_response": 2.5,
            "review_draft": 1.0,
            "escalate": 2.0,
            "final_answer": 0.0
        }
        self.billable_hours += action_costs.get(action.action_type, 1.0)

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
        # Basic context from retrieval
        if any(a.action_type == "retrieve_doc" for a in self.history):
            context.extend(self.task["knowledge_base"])
            
        # Add dynamic context from agentic actions
        if hasattr(self, 'precedent_analysis') and self.precedent_analysis:
            context.extend(self.precedent_analysis)
        
        if hasattr(self, 'client_interviews') and self.client_interviews:
            context.extend(self.client_interviews)
            
        if hasattr(self, 'draft_reviews') and self.draft_reviews:
            context.extend(self.draft_reviews)
            
        return Observation(
            user_query=self.task["query"],
            context_documents=context,
            current_step=self.current_step,
            history=[f"{a.action_type}: {a.content}" for a in self.history],
            available_actions=["classify", "retrieve_doc", "analyze_precedent", "interview_client", "draft_response", "review_draft", "escalate", "final_answer"],
            billable_hours=getattr(self, 'billable_hours', 0.0)
        )
