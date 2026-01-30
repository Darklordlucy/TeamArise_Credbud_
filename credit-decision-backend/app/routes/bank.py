from fastapi import APIRouter
from app.models.bank import BankResponse
from app.services.bank_service import bank_service
from typing import List

router = APIRouter()

@router.get("/", response_model=List[BankResponse])
async def get_all_banks():
    """Get all banks"""
    banks = await bank_service.get_all_banks()
    return banks

@router.get("/top", response_model=List[BankResponse])
async def get_top_banks(limit: int = 10):
    """Get top banks by success rate"""
    banks = await bank_service.get_top_banks(limit)
    return banks

@router.get("/trusted", response_model=List[BankResponse])
async def get_trusted_banks(limit: int = 10):
    """Get most trusted banks"""
    banks = await bank_service.get_trusted_banks(limit)
    return banks
