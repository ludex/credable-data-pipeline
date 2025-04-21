from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = "secret123"
api_key_header = APIKeyHeader(name="Authorization")

def verify_token(api_key: str = Security(api_key_header)):
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return api_key