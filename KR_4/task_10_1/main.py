from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(title="KR_4 Task 10.1")

PRODUCTS = {
    1: {"id": 1, "title": "Notebook", "count": 5},
    2: {"id": 2, "title": "Headphones", "count": 2},
}


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class CustomExceptionA(Exception):
    def __init__(self, message: str = "Requested count is too large") -> None:
        self.status_code = 409
        self.message = message
        super().__init__(message)


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Product was not found") -> None:
        self.status_code = 404
        self.message = message
        super().__init__(message)


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(_: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.message, status_code=exc.status_code).model_dump(),
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(_: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.message, status_code=exc.status_code).model_dump(),
    )


@app.get("/demo/limit", response_model=dict)
def check_limit(count: int):
    if count > 10:
        raise CustomExceptionA("You can request at most 10 items")
    return {"message": "Limit check passed", "count": count}


@app.get(
    "/demo/product/{product_id}",
    responses={404: {"model": ErrorResponse}},
)
def get_product(product_id: int):
    product = PRODUCTS.get(product_id)
    if product is None:
        raise CustomExceptionB(f"Product with id={product_id} was not found")
    return product
