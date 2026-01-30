from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_user, security
from app.models.user import UserResponse
from app.db.repositories.user_repository import user_repository

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Get current user information"""
    return user

@router.get("/financial-behavior/{user_id}")
async def get_user_financial_behavior(
    user_id: str,
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Get user's financial behavior"""
    if str(user['id']) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    from app.db.repositories.transaction_repository import transaction_repository
    behavior = transaction_repository.get_financial_behavior(user_id)
    
    if not behavior:
        return {
            "message": "No financial behavior data available",
            "status": "not_analyzed"
        }
    
    return behavior
