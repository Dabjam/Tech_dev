import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

from models import User, UserInDB

app = FastAPI(title="KR 3 - Task 6.2")
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db: dict[str, UserInDB] = {}


def get_user_by_username(username: str) -> UserInDB | None:
    for stored_username, user in fake_users_db.items():
        if secrets.compare_digest(stored_username, username):
            return user
    return None


def auth_user(credentials: HTTPBasicCredentials = Depends(security)) -> UserInDB:
    user = get_user_by_username(credentials.username)
    is_valid_password = user is not None and pwd_context.verify(
        credentials.password,
        user.hashed_password,
    )

    if user is None or not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: User) -> dict[str, str]:
    if get_user_by_username(user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    user_in_db = UserInDB(
        username=user.username,
        hashed_password=pwd_context.hash(user.password),
    )
    fake_users_db[user.username] = user_in_db
    return {"message": "User registered successfully"}


@app.get("/login")
def login(user: UserInDB = Depends(auth_user)) -> dict[str, str]:
    return {"message": f"Welcome, {user.username}!"}
