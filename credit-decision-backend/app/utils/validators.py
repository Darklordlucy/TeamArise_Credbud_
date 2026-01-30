import re
from typing import Optional
from datetime import date

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

def validate_city_tier(tier: str) -> bool:
    """Validate city tier"""
    return tier in ['tier_1', 'tier_2', 'tier_3']

def validate_positive_amount(amount: float) -> bool:
    """Validate positive amount"""
    return amount > 0

def validate_date_of_birth(dob: date) -> bool:
    """Validate date of birth (must be 18+)"""
    from datetime import datetime
    today = datetime.now().date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age >= 18
