from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import auth_service
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    result = await auth_service.register_user(user_data.dict())
    return result

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    result = await auth_service.login_user(credentials.email, credentials.password)
    return result

@router.get("/verify")
async def verify_token(user = Depends(get_current_user)):
    """Verify JWT token"""
    return {"valid": True, "user": user}
