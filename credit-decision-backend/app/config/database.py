from supabase import create_client, Client
from app.config.settings import settings

def get_supabase_client() -> Client:
    """Create and return Supabase client"""
    supabase: Client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )
    return supabase

# Create global client instance
supabase_client = get_supabase_client()
