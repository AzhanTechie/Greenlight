from pydantic import BaseModel
from typing import Optional, Literal

class Finding(BaseModel):
    quote: str
    category: Literal["Tone", "Terminology", "Claims", "Messaging"]
    severity: Literal["Low", "Medium", "High"]
    rule_id: Optional[str] = None
    fact_id: Optional[str] = None
    explanation: str
    suggestion: str

class ReviewResult(BaseModel):
    findings: list[Finding]