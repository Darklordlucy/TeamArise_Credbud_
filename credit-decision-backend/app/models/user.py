from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str = Field(..., pattern=r'^\d{10}$')
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    city_tier: str = Field(..., pattern=r'^(tier_1|tier_2|tier_3)$')

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: str
    date_of_birth: Optional[date]
    address: Optional[str]
    city_tier: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
