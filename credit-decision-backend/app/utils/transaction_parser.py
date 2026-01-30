import pandas as pd
from typing import List, Dict
from fastapi import UploadFile, HTTPException
import io

class TransactionParser:
    ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls']
    
    async def parse_file(self, file: UploadFile) -> List[Dict]:
        """Parse CSV or Excel file to transaction list"""
        # Check file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}")
        
        # Read file content
        content = await file.read()
        
        try:
            # Parse based on file type
            if file_ext == 'csv':
                df = pd.read_csv(io.BytesIO(content))
            else:
                df = pd.read_excel(io.BytesIO(content))
            
            # Validate required columns
            required_columns = ['date', 'description', 'amount', 'type']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required columns: {', '.join(missing_columns)}"
                )
            
            # Convert to list of dicts
            transactions = df.to_dict('records')
            
            # Clean and validate
            cleaned_transactions = []
            for trans in transactions:
                try:
                    cleaned_transactions.append({
                        'date': str(trans['date']),
                        'description': str(trans['description']),
                        'amount': float(trans['amount']),
                        'type': str(trans['type']).lower()
                    })
                except (ValueError, KeyError) as e:
                    continue  # Skip invalid rows
            
            return cleaned_transactions
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

transaction_parser = TransactionParser()
