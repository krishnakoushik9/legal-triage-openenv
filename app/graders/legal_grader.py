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
            return 0.0
            
        final_response = history[-1].content if history[-1].action_type == "final_answer" else ""
        if not final_response:
            # Try to find the last action that has substantial content
            for action in reversed(history):
                if action.content.strip():
                    final_response = action.content
                    break

        case = task.get("case_data", {})
        task_type = task["difficulty"]
        
        # Combine all action contents for context where needed
        full_response = " ".join([a.content for a in history])

        if task_type == "easy":
            # Classification
            score = 0.0
            
            # correct_category: 0.50
            if case.get("expected_classification") and re.search(r'\b' + re.escape(case["expected_classification"]) + r'\b', full_response, re.IGNORECASE):
                score += 0.50
                
            # jurisdiction_noted: 0.20
            jurisdiction = case.get("jurisdiction", "")
            if jurisdiction:
                jurisdiction_words = [w for w in jurisdiction.replace(',', ' ').split() if len(w) > 3]
                if any(w.lower() in full_response.lower() for w in jurisdiction_words):
                    score += 0.20
                    
            # urgency_assessed: 0.20
            urgency_words = ["low", "medium", "high", "critical", "urgent", "immediate"]
            if any(w in full_response.lower() for w in urgency_words):
                score += 0.20
                
            # reasoning_present: 0.10
            if len(re.split(r'[.!?]+', final_response)) >= 2:
                score += 0.10
                
            return round(score, 2)
            
        elif task_type == "medium":
            # Retrieval
            score = 0.0
            
            # statute_cited: 0.40
            relevant_statutes = case.get("relevant_statutes", [])
            statute_cited = False
            for stat in relevant_statutes:
                # Basic matching: check if any significant part of the statute name is present
                parts = stat.split()
                if len(parts) > 1 and any(p.lower() in full_response.lower() for p in parts if len(p) > 3):
                    statute_cited = True
                    break
            if statute_cited:
                score += 0.40
                
            # precedent_referenced: 0.25
            prior_precedents = case.get("prior_precedents", [])
            precedent_referenced = False
            for prec in prior_precedents:
                prec_name = prec.split('(')[0].strip() # remove year for matching
                if prec_name.lower() in full_response.lower():
                    precedent_referenced = True
                    break
            if precedent_referenced:
                score += 0.25
                
            # facts_addressed: 0.20
            facts = case.get("facts", "")
            fact_words = [w for w in facts.split() if len(w) > 5]
            matched_facts = sum(1 for w in fact_words if w.lower() in final_response.lower())
            if len(fact_words) > 0 and matched_facts >= 2:
                score += 0.20
                
            # reasoning_chain: 0.15
            if len(re.split(r'[.!?]+', final_response)) >= 3:
                score += 0.15
                
            return round(score, 2)
            
        elif task_type == "hard":
            # Resolution
            score = 0.0
            
            # resolution_elements_covered: 0.40
            expected_resolution_elements = case.get("expected_resolution_elements", [])
            matched_elements = []
            if expected_resolution_elements:
                for e in expected_resolution_elements:
                    # Check if any significant word of the element is in the response
                    if any(word.lower() in full_response.lower() for word in e.split() if len(word) > 4):
                        matched_elements.append(e)
                score += (len(matched_elements) / len(expected_resolution_elements)) * 0.40
                
            # statute_cited: 0.20
            relevant_statutes = case.get("relevant_statutes", [])
            statute_cited = False
            for stat in relevant_statutes:
                parts = stat.split()
                if len(parts) > 1 and any(p.lower() in full_response.lower() for p in parts if len(p) > 3):
                    statute_cited = True
                    break
            if statute_cited:
                score += 0.20
                
            # relief_addressed: 0.20
            relief_sought = case.get("relief_sought", "")
            relief_words = [w for w in relief_sought.split() if len(w) > 4]
            if relief_words and any(w.lower() in final_response.lower() for w in relief_words):
                score += 0.20
                
            # structured_format: 0.10
            if re.search(r'\d+\.|\n-', final_response):
                score += 0.10
                
            # word_count_adequate: 0.10
            if len(final_response.split()) >= 80:
                score += 0.10
                
            return round(score, 2)
            
        return 0.0

def grade(response: str, case: dict, task_type: str) -> float:
    # Standalone function for sanity testing and direct access
    grader = LegalGrader()
    # Mocking history for direct evaluation
    mock_action = Action(action_type="final_answer", content=response)
    task = {"case_data": case, "difficulty": task_type}
    return grader.grade(task, [mock_action])
