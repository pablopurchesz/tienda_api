from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    customer_email: EmailStr
    product_id: int
    quantity: int = Field(..., gt=0)
    status: Optional[OrderStatus] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderOut(BaseModel):
    id: int
    customer_email: EmailStr
    product_id: int
    quantity: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
