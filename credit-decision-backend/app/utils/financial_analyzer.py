from typing import List, Dict, Tuple
from app.config.settings import settings
from datetime import datetime, timedelta
import re

class FinancialAnalyzer:
    # Category keywords for classification
    CATEGORY_KEYWORDS = {
        'transport': ['uber', 'ola', 'metro', 'bus', 'petrol', 'diesel', 'fuel', 'parking', 'taxi', 'auto'],
        'education': ['school', 'college', 'university', 'course', 'tuition', 'book', 'education', 'study'],
        'medical': ['hospital', 'clinic', 'doctor', 'pharmacy', 'medicine', 'medical', 'health'],
        'food_shopping': ['restaurant', 'cafe', 'zomato', 'swiggy', 'food', 'mall', 'shopping', 'amazon', 'flipkart'],
        'groceries': ['grocery', 'supermarket', 'mart', 'vegetable', 'fruits', 'dmart', 'bigbazaar'],
        'emi': ['emi', 'loan', 'credit card', 'installment', 'finance'],
        'entertainment': ['movie', 'cinema', 'netflix', 'spotify', 'gaming', 'entertainment', 'concert'],
    }
    
    def __init__(self):
        self.thresholds = {
            'transport': settings.TRANSPORT_THRESHOLD / 100,
            'education': settings.EDUCATION_THRESHOLD / 100,
            'medical': settings.MEDICAL_THRESHOLD / 100,
            'food_shopping': settings.FOOD_SHOPPING_THRESHOLD / 100,
            'groceries': settings.GROCERIES_THRESHOLD / 100,
            'emi': settings.EMI_THRESHOLD / 100,
            'entertainment': settings.ENTERTAINMENT_THRESHOLD / 100,
            'others': settings.OTHERS_THRESHOLD / 100
        }
    
    def categorize_transaction(self, description: str) -> str:
        """Categorize transaction based on description"""
        description = description.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in description for keyword in keywords):
                return category
        
        return 'others'
    
    def analyze_transactions(self, transactions: List[Dict], monthly_income: float) -> Dict:
        """Analyze financial behavior from transactions"""
        # Categorize all transactions
        for trans in transactions:
            if trans['type'] == 'debit':
                trans['category'] = self.categorize_transaction(trans['description'])
        
        # Calculate category-wise spending
        category_spending = {cat: 0.0 for cat in self.thresholds.keys()}
        total_spending = 0.0
        total_income = 0.0
        
        for trans in transactions:
            if trans['type'] == 'debit':
                category = trans.get('category', 'others')
                amount = abs(trans['amount'])
                category_spending[category] += amount
                total_spending += amount
            elif trans['type'] == 'credit':
                total_income += trans['amount']
        
        # Calculate percentages and scores
        category_scores = {}
        points = 0
        
        for category, spending in category_spending.items():
            percentage = (spending / monthly_income) if monthly_income > 0 else 0
            threshold = self.thresholds[category]
            
            # Award point if within threshold
            point = 1 if percentage <= threshold else 0
            points += point
            
            category_scores[category] = {
                'spending': round(spending, 2),
                'percentage': round(percentage * 100, 2),
                'threshold': round(threshold * 100, 2),
                'point': point
            }
        
        # Determine behavior rating
        if points >= 7:
            behavior_rating = 'good'
        elif points >= 4:
            behavior_rating = 'average'
        else:
            behavior_rating = 'bad'
        
        # Additional metrics
        cash_inflow_pattern = self._analyze_inflow_pattern(transactions)
        liquidity_resilience_days = self._calculate_liquidity_resilience(transactions, total_spending)
        transaction_depth_days = self._calculate_transaction_depth(transactions)
        has_stable_inflow = self._check_stable_inflow(transactions)
        
        return {
            'total_score': points,
            'behavior_rating': behavior_rating,
            'category_scores': category_scores,
            'cash_inflow_pattern': cash_inflow_pattern,
            'liquidity_resilience_days': liquidity_resilience_days,
            'transaction_depth_days': transaction_depth_days,
            'has_stable_inflow': has_stable_inflow
        }
    
    def _analyze_inflow_pattern(self, transactions: List[Dict]) -> str:
        """Analyze if inflow is recurring"""
        credit_transactions = [t for t in transactions if t['type'] == 'credit']
        if len(credit_transactions) >= 3:
            return "recurring"
        return "irregular"
    
    def _calculate_liquidity_resilience(self, transactions: List[Dict], avg_monthly_spending: float) -> int:
        """Calculate how many days user can survive without income"""
        credit_sum = sum(t['amount'] for t in transactions if t['type'] == 'credit')
        debit_sum = sum(abs(t['amount']) for t in transactions if t['type'] == 'debit')
        
        balance = credit_sum - debit_sum
        daily_spending = avg_monthly_spending / 30 if avg_monthly_spending > 0 else 0
        
        if daily_spending > 0:
            resilience_days = int(balance / daily_spending)
            return max(0, resilience_days)
        return 0
    
    def _calculate_transaction_depth(self, transactions: List[Dict]) -> int:
        """Calculate number of days covered by transaction history"""
        if not transactions:
            return 0
        
        dates = [datetime.fromisoformat(t['date'].split()[0]) if isinstance(t['date'], str) else t['date'] for t in transactions]
        if dates:
            date_range = (max(dates) - min(dates)).days
            return date_range
        return 0
    
    def _check_stable_inflow(self, transactions: List[Dict]) -> bool:
        """Check if there's stable monthly inflow"""
        credit_transactions = [t for t in transactions if t['type'] == 'credit']
        return len(credit_transactions) >= 2

financial_analyzer = FinancialAnalyzer()
