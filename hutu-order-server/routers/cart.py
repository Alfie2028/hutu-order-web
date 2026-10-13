"""购物车接口：增删改查（均需登录）"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import CartItem, Product, User
from schemas import CartItemIn, CartItemOut, CartItemUpdate
from utils import ok

router = APIRouter(prefix="/api/cart", tags=["购物车"])


def _to_out(item: CartItem) -> dict:
    return CartItemOut.model_validate(item).model_dump(mode="json")


@router.get("")
def list_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).order_by(CartItem.created_at.desc()).all()
    return ok([_to_out(i) for i in items])


@router.post("")
def add_to_cart(body: CartItemIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Product, body.product_id):
        raise HTTPException(status_code=404, detail="商品不存在")
    options = body.options or "[]"
    # 同商品同规格则合并数量
    existing = db.query(CartItem).filter(
        CartItem.user_id == user.id, CartItem.product_id == body.product_id, CartItem.options == options
    ).first()
    if existing:
        existing.quantity += body.quantity
        db.commit()
        db.refresh(existing)
        return ok(_to_out(existing))
    item = CartItem(user_id=user.id, product_id=body.product_id, quantity=body.quantity, options=options)
    db.add(item)
    db.commit()
    db.refresh(item)
    return ok(_to_out(item))


@router.put("/{item_id}")
def update_cart(item_id: int, body: CartItemUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(CartItem, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="购物车项不存在")
    if body.quantity <= 0:
        db.delete(item)
        db.commit()
        return ok({"deleted": True})
    item.quantity = body.quantity
    db.commit()
    db.refresh(item)
    return ok(_to_out(item))


@router.delete("/{item_id}")
def delete_cart(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(CartItem, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="购物车项不存在")
    db.delete(item)
    db.commit()
    return ok({"deleted": True})


@router.delete("")
def clear_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    return ok({"cleared": True})
