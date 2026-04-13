import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import DOCS_PASSWORD, DOCS_USER, MODE

app = FastAPI(
    title="KR 3 - Task 6.3",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
security = HTTPBasic()


def verify_docs_access(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    is_valid_user = secrets.compare_digest(credentials.username, DOCS_USER)
    is_valid_password = secrets.compare_digest(credentials.password, DOCS_PASSWORD)

    if not (is_valid_user and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid docs credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/")
def index() -> dict[str, str]:
    return {"mode": MODE, "message": "Application is running"}


if MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    def custom_swagger(_: str = Depends(verify_docs_access)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="Protected docs")


    @app.get("/openapi.json", include_in_schema=False)
    def openapi_schema(_: str = Depends(verify_docs_access)):
        return JSONResponse(app.openapi())


    @app.get("/redoc", include_in_schema=False)
    def hidden_redoc():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
else:
    @app.get("/docs", include_in_schema=False)
    def disabled_docs():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


    @app.get("/openapi.json", include_in_schema=False)
    def disabled_openapi():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


    @app.get("/redoc", include_in_schema=False)
    def disabled_redoc():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
