from app.db.repositories.user_repository import user_repository
from app.utils.security import create_access_token, verify_password, hash_password
from fastapi import HTTPException, status
from typing import Dict, Optional

class AuthService:
    async def register_user(self, user_data: Dict) -> Dict:
        """Register a new user"""
        # Check if email exists
        existing_user = user_repository.get_user_by_email(user_data['email'])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        user_data['password_hash'] = hash_password(user_data['password'])
        if 'password' in user_data:
            del user_data['password']
        
        # Create user
        user = user_repository.create_user(user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Create token
        token = create_access_token(data={"sub": str(user['id'])})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    async def login_user(self, email: str, password: str) -> Dict:
        """Login user"""
        user = user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create token
        token = create_access_token(data={"sub": str(user['id'])})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

auth_service = AuthService()
