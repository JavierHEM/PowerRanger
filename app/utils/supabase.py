from supabase import create_client, Client
from app.config import settings

def get_supabase_client() -> Client:
    """
    Crea y retorna un cliente de Supabase
    """
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    
    if not url or not key:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados en las variables de entorno")
    
    supabase = create_client(url, key)
    return supabase