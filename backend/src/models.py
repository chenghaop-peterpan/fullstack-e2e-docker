from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from src.database import Base


class ExpenseItem(Base):
    __tablename__ = "expense_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="3C周邊")
    created_at = Column(DateTime, default=datetime.now)
