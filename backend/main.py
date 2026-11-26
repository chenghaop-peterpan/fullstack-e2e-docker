from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db, initialize_database
from src.models import ExpenseItem
from src.schemas import ItemCreate, ItemUpdate

initialize_database()

app = FastAPI(title="Fullstack Expense Manager API", version="1.0.0")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# 1. GET：取得所有消費項目與總金額統計
@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(ExpenseItem).order_by(ExpenseItem.id.asc()).all()
    total_amount = sum(i.amount for i in items)
    return {
        "count": len(items),
        "total_amount": total_amount,
        "items": items,
    }


# 2. POST：新增消費項目
@app.post("/items", status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    new_item = ExpenseItem(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# 3. PUT：修改消費項目（名稱、金額或分類）
@app.put("/items/{item_id}")
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ExpenseItem).filter(ExpenseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="找不到指定的項目")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


# 4. DELETE：刪除消費項目
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ExpenseItem).filter(ExpenseItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="找不到指定的項目")

    db.delete(item)
    db.commit()
    return {"message": f"項目 #{item_id} 已刪除"}