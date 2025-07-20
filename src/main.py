
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from auth import authenticate_request

app = FastAPI()


origins = ["*"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path in ["/"]:
                return await call_next(request)
            user = await authenticate_request(request)
            request.state.user = user
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": "Internal Server Error"})




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/user")
async def protected_route(request: Request):
    try:
        user = getattr(request.state, "user", None)
        if not user:
            return {"error": "Not authorized"}
        return {"message": "This is a protected route", "user": user}
    except Exception:
        return {"error": "Internal Server Error"}