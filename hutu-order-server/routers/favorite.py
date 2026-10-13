"""收藏接口：列表 / 切换"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Favorite, Product, User
from utils import ok

router = APIRouter(prefix="/api/favorites", tags=["收藏"])


@router.get("")
def list_favorites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    favorites = db.query(Favorite).filter(Favorite.user_id == user.id).all()
    return ok([f.product_id for f in favorites])


@router.post("/toggle/{product_id}")
def toggle_favorite(product_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Product, product_id):
        raise HTTPException(status_code=404, detail="商品不存在")
    favorite = db.query(Favorite).filter(
        Favorite.user_id == user.id, Favorite.product_id == product_id
    ).first()
    if favorite:
        db.delete(favorite)
        db.commit()
        return ok({"favorited": False})
    db.add(Favorite(user_id=user.id, product_id=product_id))
    db.commit()
    return ok({"favorited": True})
