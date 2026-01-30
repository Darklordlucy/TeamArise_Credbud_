from app.config.database import supabase_client
from typing import List, Dict, Optional
from uuid import UUID

class LoanRepository:
    def __init__(self):
        self.db = supabase_client
    
    def create_loan_application(self, loan_data: Dict) -> Dict:
        """Create new loan application"""
        response = self.db.table('loan_applications').insert(loan_data).execute()
        return response.data[0] if response.data else None
    
    def get_loan_by_id(self, loan_id: UUID) -> Optional[Dict]:
        """Get loan application by ID"""
        response = self.db.table('loan_applications').select('*').eq('id', str(loan_id)).execute()
        return response.data[0] if response.data else None
    
    def get_user_loans(self, user_id: UUID) -> List[Dict]:
        """Get all loans for a user"""
        response = self.db.table('loan_applications').select('*').eq('user_id', str(user_id)).order('created_at', desc=True).execute()
        return response.data if response.data else []
    
    def update_loan_decision(self, loan_id: UUID, decision_data: Dict) -> Dict:
        """Update loan with ML decision"""
        response = self.db.table('loan_applications').update(decision_data).eq('id', str(loan_id)).execute()
        return response.data[0] if response.data else None

loan_repository = LoanRepository()
