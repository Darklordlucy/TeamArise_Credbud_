from app.db.repositories.bank_repository import bank_repository
from typing import List, Dict

class BankService:
    async def get_all_banks(self) -> List[Dict]:
        """Get all banks"""
        return bank_repository.get_all_banks()
    
    async def get_top_banks(self, limit: int = 10) -> List[Dict]:
        """Get top banks"""
        return bank_repository.get_top_banks(limit)
    
    async def get_trusted_banks(self, limit: int = 10) -> List[Dict]:
        """Get trusted banks"""
        return bank_repository.get_trusted_banks(limit)

bank_service = BankService()
