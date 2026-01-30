# Loan status constants
LOAN_STATUS_PENDING = "pending"
LOAN_STATUS_PROCESSING = "processing"
LOAN_STATUS_APPROVED = "approved"
LOAN_STATUS_REJECTED = "rejected"

# Behavior ratings
BEHAVIOR_GOOD = "good"
BEHAVIOR_AVERAGE = "average"
BEHAVIOR_BAD = "bad"

# City tiers
TIER_1 = "tier_1"
TIER_2 = "tier_2"
TIER_3 = "tier_3"

# Transaction types
TRANSACTION_DEBIT = "debit"
TRANSACTION_CREDIT = "credit"

# File upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = [
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
]
