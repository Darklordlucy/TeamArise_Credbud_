from app.config.database import supabase_client
import json
from datetime import datetime

def backup_database():
    """Backup all tables to JSON files"""
    tables = ['users', 'loan_applications', 'transactions', 'financial_behavior', 'banks']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for table in tables:
        data = supabase_client.table(table).select('*').execute()
        filename = f"backup_{table}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data.data, f, indent=2, default=str)
        print(f"Backed up {table} to {filename}")

if __name__ == "__main__":
    backup_database()
