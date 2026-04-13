import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(title="KR 3 - Task 6.1")
security = HTTPBasic()

fake_users_db = {
    "admin": "admin123",
    "student": "qwerty",
}


def verify_basic_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    password = fake_users_db.get(credentials.username)
    is_valid_username = credentials.username in fake_users_db
    is_valid_password = password is not None and secrets.compare_digest(
        credentials.password,
        password,
    )

    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/login")
def login(_: str = Depends(verify_basic_user)) -> dict[str, str]:
    return {"message": "You got my secret, welcome"}
