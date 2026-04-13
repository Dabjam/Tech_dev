import secrets
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

app = FastAPI(title="KR 3 - Task 6.5")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SECRET_KEY = "jwt-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db: dict[str, str] = {}
security = HTTPBearer(auto_error=False)


class UserCredentials(BaseModel):
    username: str
    password: str


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(_: Request, __: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests"},
    )


def find_username(username: str) -> str | None:
    for stored_username in fake_users_db:
        if secrets.compare_digest(stored_username, username):
            return stored_username
    return None


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return username


@app.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
def register(request: Request, user: UserCredentials) -> dict[str, str]:
    if find_username(user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    fake_users_db[user.username] = pwd_context.hash(user.password)
    return {"message": "New user created"}


@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, user: UserCredentials) -> dict[str, str]:
    stored_username = find_username(user.username)
    if stored_username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    hashed_password = fake_users_db[stored_username]
    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization failed",
        )

    token = create_access_token(stored_username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected_resource")
def protected_resource(_: str = Depends(get_current_user)) -> dict[str, str]:
    return {"message": "Access granted"}
