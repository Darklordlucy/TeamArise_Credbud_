from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BankResponse(BaseModel):
    id: UUID
    name: str
    logo_url: Optional[str]
    avg_approval_time: str
    success_rate: float
    interest_rate_min: float
    interest_rate_max: float
    trust_score: float
    total_loans: int
    rating: float
