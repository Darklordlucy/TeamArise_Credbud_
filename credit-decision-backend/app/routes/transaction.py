from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.models.transaction import TransactionUploadResponse, FinancialBehaviorResponse
from app.services.transaction_service import transaction_service
from app.middleware.auth_middleware import get_current_user, security

router = APIRouter()

@router.post("/upload", response_model=TransactionUploadResponse)
async def upload_transactions(
    file: UploadFile = File(...),
    monthly_income: float = Form(...),
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Upload and analyze transaction history"""
    result = await transaction_service.process_transaction_upload(
        user['id'],
        file,
        monthly_income
    )
    return result

@router.get("/analyze/{user_id}", response_model=FinancialBehaviorResponse)
async def get_financial_behavior(
    user_id: str,
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Get financial behavior analysis"""
    # Ensure user can only access their own data
    if str(user['id']) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = await transaction_service.get_financial_behavior(user_id)
    return result
