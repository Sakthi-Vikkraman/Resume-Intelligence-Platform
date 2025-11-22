from pydantic import BaseModel
from typing import Optional, Dict, Any

class SuitabilityMetrics(BaseModel):
    semantic_similarity: float
    skill_overlap: float
    experience_score: float
    suitability_score: float

class EvaluateResponse(BaseModel):
    jd_name: str
    metrics: SuitabilityMetrics
    verdict: str
    replaced_best: bool
    previous_best: Optional[Dict[str, Any]] = None
    memory_summary: Dict[str, Any]
