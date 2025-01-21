from pydantic import BaseModel, validator
from typing import List
from models import RoleEnum


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum

    @validator("role", pre=True)
    def normalize_role(cls, value):
        normalized_value = value.lower()
        if normalized_value not in RoleEnum._value2member_map_:
            raise ValueError("Rol 'admin' yoki 'mijoz' bo'lishi kerak.")
        return normalized_value


class ProductCreateSchema(BaseModel):
    name: str
    price: float
    stock: int

    class Config:
        orm_mode = True

    @validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Narx 0 dan katta bo'lishi kerak.")
        return v

    @validator("stock")
    def validate_stock(cls, v):
        if v <= 0:
            raise ValueError("Stok 0 dan katta bo'lishi kerak.")
        return v
    

class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    class Config:
        orm_mode = True
    

class OrderDetailSchema(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    items: List[OrderDetailSchema]

    class Config:
        orm_mode = True


class OrderResponseSchema(BaseModel):
    id: int
    customer_id: int
    status: str
    items: List[OrderDetailSchema]

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True