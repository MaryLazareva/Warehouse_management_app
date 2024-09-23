from pydantic import BaseModel, ConfigDict
from typing import List


class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    amount_all: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateSchema(BaseModel):
    name: str
    description: str
    price: float
    amount_all: int

    model_config = ConfigDict(from_attributes=True)
  


class OrderCreateSchema(BaseModel):
    status: str
    products: List[int]
    amounts: List[int]

    model_config = ConfigDict(from_attributes=True)  # Для работы с объектами ORM


class OrderUpdateStatusSchema(BaseModel):
    status: str

    model_config = ConfigDict(from_attributes=True)
