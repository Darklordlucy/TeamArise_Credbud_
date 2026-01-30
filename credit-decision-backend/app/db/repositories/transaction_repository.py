from app.config.database import supabase_client
from typing import Dict, List, Optional
from uuid import UUID

class TransactionRepository:
    def __init__(self):
        self.db = supabase_client
    
    def create_transaction(self, transaction_data: Dict) -> Dict:
        """Save transaction data"""
        response = self.db.table('transactions').insert(transaction_data).execute()
        return response.data[0] if response.data else None
    
    def get_user_transactions(self, user_id: UUID) -> List[Dict]:
        """Get all transactions for a user"""
        response = self.db.table('transactions').select('*').eq('user_id', str(user_id)).order('upload_date', desc=True).execute()
        return response.data if response.data else []
    
    def save_financial_behavior(self, behavior_data: Dict) -> Dict:
        """Save financial behavior analysis"""
        response = self.db.table('financial_behavior').insert(behavior_data).execute()
        return response.data[0] if response.data else None
    
    def get_financial_behavior(self, user_id: UUID) -> Optional[Dict]:
        """Get latest financial behavior for user"""
        response = self.db.table('financial_behavior').select('*').eq('user_id', str(user_id)).order('created_at', desc=True).limit(1).execute()
        return response.data[0] if response.data else None

transaction_repository = TransactionRepository()
