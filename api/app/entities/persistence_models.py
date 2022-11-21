from pydantic import BaseModel
from typing import List, Optional


class UserCreationPersistenceModel(BaseModel):
    id: str
    user_name: str
    password: str
    group_id: str
    role_ids: List[str]
    email: str
    update_at: int
    created_at: int
    modified_by: Optional[str]


class ProductsPersistenceModel(BaseModel):
    id: str
    serial_number: str
    model: str
    brand: str
    price: float
    name: str
    sku: str
    updated_at: int
    created_at: int
