import abc
from typing import Dict, Any
from app.models import Action
import re

class BaseGrader(abc.ABC):
    @abc.abstractmethod
    def grade(self, task: Dict[str, Any], history: list[Action]) -> float:
        pass

class LegalGrader(BaseGrader):
    def grade(self, task: Dict[str, Any], history: list[Action]) -> float:
        # Re-implemented as a deterministic, multi-criteria weighted rubric grader.
        if not history:
            return 0.05
            
        final_response = history[-1].content if history[-1].action_type == "final_answer" else ""
        if not final_response:
            # Try to find the last action that has substantial content
            for action in reversed(history):
                if action.content.strip():
                    final_response = action.content
                    break

        # Base Penalty: did not finish with a final_answer action?
        last_action_is_final = history[-1].action_type == "final_answer"
        
        # Penalize if the episode didn't end with a structured final answer
        completion_multiplier = 1.0 if last_action_is_final else 0.7

        case = task.get("case_data", {})
        task_type = task["difficulty"]
        
        # Combine all action contents for context where needed
        full_response = " ".join([a.content for a in history])

        # Check for retrieval usage
        has_retrieved = any(a.action_type == "retrieve_doc" for a in history)
        
        # Calculate billable hours penalty (if trackable from history length heuristically, or we can just penalize long histories)
        action_costs = {
            "classify": 0.5, "retrieve_doc": 1.0, "analyze_precedent": 2.0,
            "interview_client": 1.5, "draft_response": 2.5, "review_draft": 1.0,
            "escalate": 2.0, "final_answer": 0.0
        }
        total_hours = sum(action_costs.get(a.action_type, 1.0) for a in history)
        # Efficiency multiplier: drops if hours > 10
        efficiency_multiplier = max(0.8, 1.0 - max(0, total_hours - 10.0) * 0.02)

        if task_type == "easy":
            score = 0.0
            expected = case.get("expected_classification", "")
            if expected and re.search(r'\b' + re.escape(expected) + r'\b', full_response, re.IGNORECASE):
                score += 0.50
            jurisdiction = case.get("jurisdiction", "")
            if jurisdiction:
                jurisdiction_parts = [p.strip() for p in jurisdiction.split(',') if len(p.strip()) > 2]
                if any(p.lower() in full_response.lower() for p in jurisdiction_parts):
                    score += 0.20
            urgency = case.get("urgency", "low")
            if re.search(r'\b' + re.escape(urgency) + r'\b', full_response, re.IGNORECASE):
                score += 0.20
            elif any(w in full_response.lower() for w in ["urgent", "immediate", "low priority"]):
                score += 0.10
            if len(re.split(r'[.!?]+', final_response)) >= 2 and len(final_response.split()) > 20:
                score += 0.10
            
            raw_score = score * completion_multiplier * efficiency_multiplier
            return round(max(0.01, min(0.99, raw_score)), 2)
            
        elif task_type == "medium":
            score = 0.0
            if not has_retrieved:
                score -= 0.1
            else:
                score += 0.1
            relevant_statutes = case.get("relevant_statutes", [])
            statutes_found = 0
            for stat in relevant_statutes:
                if stat.lower() in full_response.lower():
                    statutes_found += 1
            if statutes_found >= 1:
                score += 0.40
            prior_precedents = case.get("prior_precedents", [])
            precedent_referenced = False
            for prec in prior_precedents:
                prec_name = prec.split('(')[0].strip()
                if prec_name.lower() in full_response.lower():
                    precedent_referenced = True
                    break
            if precedent_referenced:
                score += 0.20
            facts = case.get("facts", "")
            fact_keywords = [w.lower() for w in facts.split() if len(w) > 6]
            matched_keywords = sum(1 for w in fact_keywords if w in final_response.lower())
            if len(fact_keywords) > 0 and matched_keywords >= 2:
                score += 0.15
            if len(re.split(r'[.!?]+', final_response)) >= 3 and len(final_response.split()) > 40:
                score += 0.15
            if any(a.action_type == "interview_client" for a in history):
                score += 0.05
                
            raw_score = score * completion_multiplier * efficiency_multiplier
            return round(max(0.01, min(0.99, raw_score)), 2)
            
        elif task_type == "hard":
            score = 0.0
            if not has_retrieved:
                score -= 0.2
            else:
                score += 0.05
            if any(a.action_type == "analyze_precedent" for a in history): score += 0.05
            if any(a.action_type == "escalate" for a in history): score += 0.05
            if any(a.action_type == "interview_client" for a in history): score += 0.05
            if any(a.action_type == "review_draft" for a in history): score += 0.05
            expected_resolution_elements = case.get("expected_resolution_elements", [])
            matched_elements = 0
            if expected_resolution_elements:
                for e in expected_resolution_elements:
                    if e.lower() in full_response.lower():
                        matched_elements += 1
                score += (matched_elements / len(expected_resolution_elements)) * 0.25
            relevant_statutes = case.get("relevant_statutes", [])
            prior_precedents = case.get("prior_precedents", [])
            has_stat = any(s.lower() in full_response.lower() for s in relevant_statutes)
            has_prec = any(p.split('(')[0].strip().lower() in full_response.lower() for p in prior_precedents)
            if has_stat: score += 0.15
            if has_prec: score += 0.10
            relief_sought = case.get("relief_sought", "")
            if len(relief_sought) > 5 and any(w.lower() in final_response.lower() for w in relief_sought.split() if len(w) > 5):
                score += 0.10
            if re.search(r'\d+\.|\n-', final_response) and len(final_response.split()) > 100:
                score += 0.05
            reasoning_keywords = ["therefore", "consequently", "pursuant to", "accordingly", "furthermore", "however"]
            depth_count = sum(1 for kw in reasoning_keywords if kw in final_response.lower())
            if depth_count >= 2:
                score += 0.10
                
            raw_score = score * completion_multiplier * efficiency_multiplier
            return round(max(0.01, min(0.99, raw_score)), 2)
            
        return 0.05

def grade(response: str, case: dict, task_type: str) -> float:
    grader = LegalGrader()
    mock_action = Action(action_type="final_answer", content=response)
    task = {"case_data": case, "difficulty": task_type}
    return grader.grade(task, [mock_action])
