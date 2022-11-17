from pydantic import BaseModel
from typing import List, Optional


class UserCreationPersistenceModel(BaseModel):
    id: str
    user_name: str
    group_id: str
    role_ids: List[str]
    email: str
    update_at: float
    created_at: float
    modified_by: Optional[str]
