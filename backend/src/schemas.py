from typing import Optional

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    amount: float
    category: Optional[str] = "飲食"


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
