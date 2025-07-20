from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
async def getUserDetails(request: Request):
    try:
        user = getattr(request.state, "user", None)
        if not user:
            return {"error": "Not authorized"}
        return {"message": "This is a protected route", "user": user}
    except Exception:
        return {"error": "Internal Server Error"}
