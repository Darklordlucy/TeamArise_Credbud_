from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    type: str  # debit or credit
    category: Optional[str] = None

class TransactionUploadResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    transactions_count: int
    upload_date: datetime
    message: str

class FinancialBehaviorResponse(BaseModel):
    id: UUID
    user_id: UUID
    total_score: int
    behavior_rating: str
    category_scores: Dict
    cash_inflow_pattern: str
    liquidity_resilience_days: int
    transaction_depth_days: int
    has_stable_inflow: bool
    created_at: datetime
