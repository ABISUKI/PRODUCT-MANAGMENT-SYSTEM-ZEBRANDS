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
    result: Optional[LoginOutput]
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
    result: Optional[UserCreationOutput]
    errors: List[str]
    timestamp: int


class GetUserOutput(BaseModel):
    user: Optional[UserCreationOutput]


class GetUserOutputBase(BaseModel):
    status: str
    result: Optional[GetUserOutput]
    errors: List[str]
    timestamp: int


class GetAllUsersOutput(BaseModel):
    users: Optional[List[UserCreationOutput]]


class GetAllUsersOutputBase(BaseModel):
    status: str
    result: Optional[GetAllUsersOutput]
    errors: List[str]
    timestamp: int


# ************** P R O D U C T S ********************************

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
    result: Optional[ProductsCreationOutput]
    errors: List[str]
    timestamp: int


class GetAllProductsOutput(BaseModel):
    products: Optional[List[ProductsCreationOutput]]


class GetAllProductsOutputBase(BaseModel):
    status: str
    result: Optional[GetAllProductsOutput]
    errors: List[str]
    timestamp: int
