# app/models.py
from pydantic import BaseModel
from typing import Optional

class UserSession(BaseModel):
    user_id: str
    event_name: Optional[str] = None
