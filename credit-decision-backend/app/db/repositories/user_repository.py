from app.config.database import supabase_client
from typing import Optional, Dict
from uuid import UUID

class UserRepository:
    def __init__(self):
        self.db = supabase_client
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        response = self.db.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        response = self.db.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_id(self, user_id: UUID) -> Optional[Dict]:
        """Get user by ID"""
        response = self.db.table('users').select('*').eq('id', str(user_id)).execute()
        return response.data[0] if response.data else None
    
    def update_user(self, user_id: UUID, update_data: Dict) -> Dict:
        """Update user information"""
        response = self.db.table('users').update(update_data).eq('id', str(user_id)).execute()
        return response.data[0] if response.data else None

user_repository = UserRepository()
