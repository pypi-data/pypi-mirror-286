from typing import Dict, Any
from pydantic import BaseModel, field_validator


class GameObject(BaseModel):
    id: str
    type: str
    attributes: Dict[str, Any] = {}
    equipment: Dict[str, 'GameObject'] = {}  # New field for equipment

    @field_validator('id', 'type')
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("must not be empty")
        return v
