from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from uuid import UUID

class LoanApplicationCreate(BaseModel):
    amount_requested: float = Field(..., gt=0)
    loan_duration: int = Field(..., gt=0) # Duration in months
    num_debts: int = Field(..., ge=0)
    total_debt_amount: float = Field(..., ge=0)
    monthly_emis: float = Field(..., ge=0)
    total_assets: float = Field(..., ge=0)
    monthly_income: float = Field(..., gt=0)
    city_tier: str = Field(..., pattern=r'^(tier_1|tier_2|tier_3)$')

class LoanApplicationResponse(BaseModel):
    id: UUID
    user_id: UUID
    application_date: datetime
    amount_requested: float
    loan_duration: Optional[int]
    num_debts: int
    total_debt_amount: float
    monthly_emis: float
    total_assets: float
    monthly_income: float
    city_tier: str
    ml_score: Optional[float]
    acceptance_rate: Optional[float]
    status: str
    feedback: Optional[Dict]
    created_at: datetime

class LoanDecisionResponse(BaseModel):
    loan_id: UUID
    acceptance_rate: float
    ml_score: float
    status: str
    feedback: Dict
    message: str
