import os
import logging
import httpx
from fastapi import Request, HTTPException

# Only load .env locally (not in production)
if os.getenv("VERCEL_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

logger = logging.getLogger("auth")
logging.basicConfig(level=logging.INFO)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment")

async def authenticate_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Missing or malformed Authorization header")
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]

    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_ANON_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)

    if response.status_code != 200:
        logger.warning(f"Supabase rejected token: {response.status_code} {response.text}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = response.json()
    logger.info("User authenticated via Supabase")
    return user
