from pydantic import BaseModel, Field
from typing import List, Literal


# to force dicipline on llm

class EmailDecision(BaseModel):
    decision: Literal["DELETE", "KEEP", "UNSURE"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    signals: List[str]
