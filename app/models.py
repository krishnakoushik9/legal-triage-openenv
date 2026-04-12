from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional, Dict, Any

class Observation(BaseModel):
    user_query: str
    context_documents: List[str] = []
    current_step: int
    history: List[str] = []
    available_actions: List[str] = ["classify", "retrieve_doc", "analyze_precedent", "interview_client", "draft_response", "review_draft", "escalate", "final_answer"]
    billable_hours: float = 0.0

class Action(BaseModel):
    action_type: Literal[
        "classify",
        "retrieve_doc",
        "analyze_precedent",
        "interview_client",
        "draft_response",
        "review_draft",
        "escalate",
        "final_answer"
    ]
    content: str

    @validator('*', pre=True)
    def strip_and_limit(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if len(v) > 5000:
                raise ValueError("Field too long — max 5000 chars")
        return v

class RewardInfo(BaseModel):
    score: float
    reason: str
    is_terminal: bool
