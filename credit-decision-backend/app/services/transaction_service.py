from app.utils.transaction_parser import transaction_parser
from app.utils.financial_analyzer import financial_analyzer
from app.db.repositories.transaction_repository import transaction_repository
from fastapi import UploadFile, HTTPException, status
from typing import Dict

class TransactionService:
    async def process_transaction_upload(self, user_id: str, file: UploadFile, monthly_income: float) -> Dict:
        """Process uploaded transaction file"""
        # Parse file
        transactions = await transaction_parser.parse_file(file)
        
        if not transactions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid transactions found in file"
            )
        
        # Save transaction data
        transaction_data = {
            'user_id': user_id,
            'file_name': file.filename,
            'transaction_data': transactions
        }
        
        saved_transaction = transaction_repository.create_transaction(transaction_data)
        
        # Analyze financial behavior
        analysis = financial_analyzer.analyze_transactions(transactions, monthly_income)
        
        # Save financial behavior
        behavior_data = {
            'user_id': user_id,
            'transaction_id': saved_transaction['id'],
            'total_score': analysis['total_score'],
            'behavior_rating': analysis['behavior_rating'],
            'category_scores': analysis['category_scores'],
            'cash_inflow_pattern': analysis['cash_inflow_pattern'],
            'liquidity_resilience_days': analysis['liquidity_resilience_days'],
            'transaction_depth_days': analysis['transaction_depth_days'],
            'has_stable_inflow': analysis['has_stable_inflow']
        }
        
        transaction_repository.save_financial_behavior(behavior_data)
        
        return {
            'id': saved_transaction['id'],
            'user_id': user_id,
            'file_name': file.filename,
            'transactions_count': len(transactions),
            'upload_date': saved_transaction['upload_date'],
            'message': f'Successfully uploaded and analyzed {len(transactions)} transactions'
        }
    
    async def get_financial_behavior(self, user_id: str) -> Dict:
        """Get latest financial behavior for user"""
        behavior = transaction_repository.get_financial_behavior(user_id)
        
        if not behavior:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No financial behavior data found. Please upload transaction history."
            )
        
        return behavior

transaction_service = TransactionService()
