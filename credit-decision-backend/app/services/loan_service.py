from app.db.repositories.loan_repository import loan_repository
from app.db.repositories.transaction_repository import transaction_repository
from app.services.ml_service import ml_service
from fastapi import HTTPException, status
from typing import Dict, List
from uuid import UUID

class LoanService:
    async def process_loan_application(self, user_id: str, loan_data: Dict) -> Dict:
        """Process a new loan application"""
        # Add user_id to loan data
        loan_data['user_id'] = user_id
        loan_data['status'] = 'processing'
        
        # Create loan application in database
        loan = loan_repository.create_loan_application(loan_data)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create loan application"
            )
        
        # Get ML prediction
        ml_result = await ml_service.predict_credit_score(loan_data)
        
        # Get financial behavior if exists
        financial_behavior = transaction_repository.get_financial_behavior(user_id)
        
        # Adjust acceptance rate based on financial behavior
        final_acceptance_rate = ml_result['acceptance_rate']
        
        if financial_behavior:
            behavior_rating = financial_behavior.get('behavior_rating', 'average')
            
            if behavior_rating == 'good':
                final_acceptance_rate += 10
            elif behavior_rating == 'bad':
                final_acceptance_rate -= 15
            
            # Add behavior insights to feedback
            ml_result['feedback']['financial_behavior'] = {
                'rating': behavior_rating,
                'score': financial_behavior.get('total_score', 0),
                'impact': 'positive' if behavior_rating == 'good' else 'negative'
            }
        else:
            ml_result['feedback']['financial_behavior'] = {
                'rating': 'not_available',
                'message': 'Upload transaction history for better evaluation'
            }
        
        # Ensure bounds
        final_acceptance_rate = max(10, min(95, final_acceptance_rate))
        
        # Update loan with decision
        decision_data = {
            'ml_score': ml_result['ml_score'],
            'acceptance_rate': round(final_acceptance_rate, 2),
            'status': ml_result['status'],
            'feedback': ml_result['feedback']
        }
        
        updated_loan = loan_repository.update_loan_decision(loan['id'], decision_data)
        
        return {
            'loan_id': updated_loan['id'],
            'acceptance_rate': round(final_acceptance_rate, 2),
            'ml_score': ml_result['ml_score'],
            'status': ml_result['status'],
            'feedback': ml_result['feedback'],
            'message': self._get_decision_message(ml_result['status'])
        }
    
    async def get_user_loans(self, user_id: str) -> List[Dict]:
        """Get all loans for a user"""
        loans = loan_repository.get_user_loans(user_id)
        return loans
    
    async def get_loan_by_id(self, loan_id: str, user_id: str) -> Dict:
        """Get a specific loan"""
        loan = loan_repository.get_loan_by_id(loan_id)
        
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        # Verify ownership
        if str(loan['user_id']) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this loan"
            )
        
        return loan
    
    def _get_decision_message(self, status: str) -> str:
        """Get user-friendly message based on status"""
        messages = {
            'approved': 'Congratulations! Your loan application has high approval chances.',
            'processing': 'Your application is under review. We may need additional information.',
            'rejected': 'Unfortunately, your application does not meet current criteria. Please review feedback.'
        }
        return messages.get(status, 'Application processed')

loan_service = LoanService()
