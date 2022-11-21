from pydantic import BaseModel, constr, EmailStr, validator
from typing import List, Optional


class UserCreationInput(BaseModel):
    user_name: constr(min_length=3)
    password: constr(min_length=3)
    group_id: constr(min_length=3)
    role_ids: List[str]
    email: EmailStr

    @validator('email', pre=True, always=False)
    def validate_e(cls, val):
        return val


class UserUpdateInput(BaseModel):
    user_name: Optional[str]
    group_id: Optional[str]
    role_ids: Optional[List[str]]
    email: Optional[str]
    user_id: str


class UserDeleteInput(BaseModel):
    user_id: constr(min_length=3)
    reason: constr(min_length=3)


class ProductsCreationInput(BaseModel):
    serial_number: constr(min_length=1)
    model: constr(min_length=1)
    brand: constr(min_length=1)
    price: float
    name: constr(min_length=1)


class ProductsUpdateInput(BaseModel):
    product_id: constr(min_length=1)
    model: Optional[str]
    brand: Optional[str]
    price: Optional[str]
    name: Optional[str]


class ProductDeleteInput(BaseModel):
    product_id: constr(min_length=1)
    reason: constr(min_length=3)
