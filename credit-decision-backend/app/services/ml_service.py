from app.ml.credit_score_model import credit_model
from typing import Dict

class MLService:
    async def predict_credit_score(self, loan_data: Dict) -> Dict:
        """Predict credit score and generate feedback"""
        # Get prediction
        ml_score, acceptance_rate = credit_model.predict(loan_data)
        
        # Generate feedback
        feedback = self._generate_feedback(loan_data, ml_score, acceptance_rate)
        
        # Determine status
        if acceptance_rate >= 70:
            status = "approved"
        elif acceptance_rate >= 50:
            status = "processing"
        else:
            status = "rejected"
        
        return {
            "ml_score": round(ml_score, 2),
            "acceptance_rate": round(acceptance_rate, 2),
            "status": status,
            "feedback": feedback
        }
    
    def _generate_feedback(self, loan_data: Dict, ml_score: float, acceptance_rate: float) -> Dict:
        """Generate detailed feedback"""
        feedback = {
            "overall": "",
            "strengths": [],
            "concerns": [],
            "recommendations": []
        }
        
        debt_to_income = loan_data['total_debt_amount'] / max(loan_data['monthly_income'] * 12, 1)
        emi_to_income = loan_data['monthly_emis'] / max(loan_data['monthly_income'], 1)
        
        # Overall message
        if acceptance_rate >= 70:
            feedback["overall"] = "Your loan application shows strong financial health and has a high probability of approval."
        elif acceptance_rate >= 50:
            feedback["overall"] = "Your application is under review. Some improvements could increase approval chances."
        else:
            feedback["overall"] = "Your application needs significant improvement before approval can be considered."
        
        # Strengths
        if loan_data['total_assets'] > loan_data['total_debt_amount']:
            feedback["strengths"].append("Strong asset-to-debt ratio")
        if emi_to_income < 0.3:
            feedback["strengths"].append("Manageable EMI obligations")
        if loan_data['num_debts'] <= 2:
            feedback["strengths"].append("Low number of existing debts")
        
        # Concerns
        if debt_to_income > 0.5:
            feedback["concerns"].append("High debt-to-income ratio")
        if emi_to_income > 0.4:
            feedback["concerns"].append("EMI burden is too high relative to income")
        if loan_data['num_debts'] > 3:
            feedback["concerns"].append("Multiple existing debt obligations")
        
        # Recommendations
        if debt_to_income > 0.5:
            feedback["recommendations"].append("Consider reducing existing debt before applying")
        if emi_to_income > 0.4:
            feedback["recommendations"].append("Try to consolidate or reduce EMI payments")
        if ml_score < 60:
            feedback["recommendations"].append("Build a stronger transaction history and maintain regular income")
        
        return feedback

ml_service = MLService()
