import secrets
from datetime import UTC, datetime, timedelta
from typing import Callable

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="KR 3 - Task 7.1")

SECRET_KEY = "rbac-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

ROLE_PERMISSIONS = {
    "admin": ["create", "read", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"],
}

fake_users_db: dict[str, dict[str, str]] = {}


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


def find_user(username: str) -> dict[str, str] | None:
    for stored_username, user in fake_users_db.items():
        if secrets.compare_digest(stored_username, username):
            return user
    return None


def create_access_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, str]:
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
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    username = payload.get("sub")
    role = payload.get("role")
    if not username or role not in ROLE_PERMISSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return {"username": username, "role": role}


def require_roles(*allowed_roles: str) -> Callable:
    def checker(user: dict[str, str] = Depends(get_current_user)) -> dict[str, str]:
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )
        return user

    return checker


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest) -> dict[str, str]:
    if data.role not in ROLE_PERMISSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported role",
        )
    if find_user(data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    fake_users_db[data.username] = {
        "username": data.username,
        "role": data.role,
        "hashed_password": pwd_context.hash(data.password),
    }
    return {"message": f"User {data.username} registered with role {data.role}"}


@app.post("/login")
def login(data: LoginRequest) -> dict[str, str]:
    user = find_user(data.username)
    if user is None or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected_resource")
def protected_resource(
    user: dict[str, str] = Depends(require_roles("admin", "user")),
) -> dict[str, str]:
    return {
        "message": "Access granted",
        "username": user["username"],
        "role": user["role"],
    }


@app.post("/admin/resource")
def create_resource(user: dict[str, str] = Depends(require_roles("admin"))) -> dict[str, str]:
    return {"message": f"Resource created by {user['username']}"}


@app.delete("/admin/resource")
def delete_resource(user: dict[str, str] = Depends(require_roles("admin"))) -> dict[str, str]:
    return {"message": f"Resource deleted by {user['username']}"}


@app.get("/user/resource")
def read_resource(
    user: dict[str, str] = Depends(require_roles("admin", "user", "guest")),
) -> dict[str, str]:
    return {
        "message": f"Readable resource for {user['username']}",
        "permissions": ROLE_PERMISSIONS[user["role"]],
    }


@app.put("/user/resource")
def update_resource(
    user: dict[str, str] = Depends(require_roles("admin", "user")),
) -> dict[str, str]:
    return {"message": f"Resource updated by {user['username']}"}
