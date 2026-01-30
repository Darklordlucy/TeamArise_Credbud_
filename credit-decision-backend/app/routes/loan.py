from fastapi import APIRouter, Depends, HTTPException, status
from app.models.loan import LoanApplicationCreate, LoanApplicationResponse, LoanDecisionResponse
from app.services.loan_service import loan_service
from app.middleware.auth_middleware import get_current_user, security
from typing import List

router = APIRouter()

@router.post("/apply", response_model=LoanDecisionResponse)
async def apply_for_loan(
    loan_data: LoanApplicationCreate,
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Apply for a new loan"""
    result = await loan_service.process_loan_application(user['id'], loan_data.dict())
    return result

@router.get("/user/{user_id}", response_model=List[LoanApplicationResponse])
async def get_user_loans(
    user_id: str,
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Get all loans for a user"""
    # Ensure user can only access their own loans
    if str(user['id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this data"
        )
    
    loans = await loan_service.get_user_loans(user_id)
    return loans

@router.get("/{loan_id}", response_model=LoanApplicationResponse)
async def get_loan_details(
    loan_id: str,
    user = Depends(get_current_user),
    credentials = Depends(security)
):
    """Get details of a specific loan"""
    loan = await loan_service.get_loan_by_id(loan_id, user['id'])
    return loan
