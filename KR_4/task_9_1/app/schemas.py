from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    price: float = Field(gt=0)
    count: int = Field(ge=0)
    description: str = Field(min_length=3, max_length=255)


class ProductRead(ProductCreate):
    id: int

    model_config = {"from_attributes": True}
