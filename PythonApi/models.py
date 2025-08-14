from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# Product Category Models
class ProductCategory(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class CreateProductCategoryCommand(BaseModel):
    name: str
    description: Optional[str] = None


class UpdateProductCategoryCommand(BaseModel):
    name: str
    description: Optional[str] = None


# Product Models
class Product(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    category: Optional[ProductCategory] = None
    stock: int = 0
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: float
        }


class CreateProductCommand(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    stock: int = 0
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: float
        }


class UpdateProductCommand(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    stock: int
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: float
        }