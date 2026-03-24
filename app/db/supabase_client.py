"""
Reusable Supabase Client
"""
import os
from supabase import create_client, Client

_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client: Client = None

def get_supabase_client() -> Client:
    """Get a singleton Supabase client instance."""
    global _client
    if _client is None:
        if not _SUPABASE_URL or not _SUPABASE_KEY:
            raise RuntimeError("Supabase credentials are not set in environment variables.")
        _client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
    return _client
