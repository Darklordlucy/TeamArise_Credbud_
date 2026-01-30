from app.config.database import supabase_client
from typing import List, Dict

class BankRepository:
    def __init__(self):
        self.db = supabase_client
    
    def get_all_banks(self) -> List[Dict]:
        """Get all banks"""
        response = self.db.table('banks').select('*').execute()
        return response.data if response.data else []
    
    def get_top_banks(self, limit: int = 10) -> List[Dict]:
        """Get top banks by success rate"""
        response = self.db.table('banks').select('*').order('success_rate', desc=True).limit(limit).execute()
        return response.data if response.data else []
    
    def get_trusted_banks(self, limit: int = 10) -> List[Dict]:
        """Get most trusted banks"""
        response = self.db.table('banks').select('*').order('trust_score', desc=True).limit(limit).execute()
        return response.data if response.data else []

bank_repository = BankRepository()
