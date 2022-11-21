from pydantic import BaseModel
from typing import List, Optional


class OutputBase(BaseModel):
    status: str
    result: dict
    errors: List[str]
    timestamp: int


class LoginOutput(BaseModel):
    access_token: str
    type: str


class LoginOutputBase(BaseModel):
    status: str
    result: LoginOutput
    errors: List[str]
    timestamp: int


class UserCreationOutput(BaseModel):
    id: str
    user_name: str
    password: str
    group_id: str
    role_ids: List[str]
    email: str
    update_at: int
    created_at: int
    modified_by: Optional[str]


class UserCreationOutputBase(BaseModel):
    status: str
    result: UserCreationOutput
    errors: List[str]
    timestamp: int


class GetUserOutputBase(BaseModel):
    status: str
    result: UserCreationOutput
    errors: List[str]
    timestamp: int


class GetAllUsersOutputBase(BaseModel):
    status: str
    result: List[UserCreationOutput]
    errors: List[str]
    timestamp: int



class ProductsCreationOutput(BaseModel):
    id: str
    serial_number: str
    model: str
    brand: str
    price: float
    name: str
    sku: str
    updated_at: int
    created_at: int


class ProductsCreationOutputBase(BaseModel):
    status: str
    result: ProductsCreationOutput
    errors: List[str]
    timestamp: int


class GetProductOutputBase(BaseModel):
    status: str
    result: ProductsCreationOutput
    errors: List[str]
    timestamp: int


class GetAllProductsOutputBase(BaseModel):
    status: str
    result: List[ProductsCreationOutput]
    errors: List[str]
    timestamp: int
