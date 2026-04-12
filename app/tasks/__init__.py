from typing import List, Dict, Any
import random
from app.models import Observation
from app.data.legal_cases import LEGAL_CASES

def get_task(difficulty: str) -> Dict[str, Any]:
    cases = [case for case in LEGAL_CASES.values() if case["difficulty"] == difficulty]
    # Set seed for reproducibility in baselines, but allow it to be random if not set
    # Actually, instructions say "use random.seed(42) for reproducibility in baseline runs" 
    # but we will just pick randomly here and assume the script sets the seed.
    case = random.choice(cases)
    
    knowledge_base = []
    for stat in case.get("relevant_statutes", []):
        text = case.get("statute_text", {}).get(stat, "No details available.")
        knowledge_base.append(f"STATUTE: {stat}\nTEXT: {text}")
    
    for prec in case.get("prior_precedents", []):
        knowledge_base.append(f"PRECEDENT: {prec}\nNote: Relevant prior case law involving similar legal issues.")

    return {
        "id": f"{difficulty}_task",
        "difficulty": difficulty,
        "expected_classification": case["expected_classification"],
        "knowledge_base": knowledge_base,
        "case_data": case,
        "query": f"Please review the following case and provide legal assistance.\n\nTitle: {case['title']}\nJurisdiction: {case['jurisdiction']}\nFacts: {case['facts']}\nParties: {case['parties']['plaintiff']} vs {case['parties']['defendant']}\nRelief Sought: {case['relief_sought']}"
    }
