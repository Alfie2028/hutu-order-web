"""评价接口：下单完成后评分 + 文字评价；商家查看全部评价"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Order, Review, User
from schemas import ReviewIn
from utils import ok

router = APIRouter(prefix="/api/reviews", tags=["评价"])


def _require_merchant(user: User):
    if user.role != "merchant":
        raise HTTPException(status_code=403, detail="无商家权限")


def _to_out(review: Review, username: str = "", order_no: str = "", store_id: str = "") -> dict:
    return {
        "id": review.id,
        "order_id": review.order_id,
        "order_no": order_no,
        "user_id": review.user_id,
        "username": username,
        "store_id": store_id,
        "rating": review.rating,
        "content": review.content,
        "created_at": review.created_at.isoformat() if review.created_at else None,
    }


@router.post("")
def create_review(body: ReviewIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """创建评价：仅订单本人、订单已完成、且未评价过"""
    if not 1 <= body.rating <= 5:
        raise HTTPException(status_code=400, detail="评分需在 1~5 星之间")
    order = db.get(Order, body.order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "completed":
        raise HTTPException(status_code=400, detail="订单完成后才能评价")
    if db.query(Review).filter(Review.order_id == order.id).first():
        raise HTTPException(status_code=400, detail="该订单已评价过")

    review = Review(order_id=order.id, user_id=user.id, rating=body.rating, content=body.content.strip())
    db.add(review)
    db.commit()
    db.refresh(review)
    return ok(_to_out(review, username=user.username, order_no=order.order_no, store_id=order.store_id))


@router.get("/mine")
def list_my_reviews(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """当前用户已提交的评价（前端据此判断订单是否已评价）"""
    reviews = db.query(Review).filter(Review.user_id == user.id).order_by(Review.created_at.desc()).all()
    orders = {o.id: o for o in db.query(Order).filter(Order.id.in_([r.order_id for r in reviews])).all()} if reviews else {}
    return ok([_to_out(r, username=user.username, order_no=(orders.get(r.order_id).order_no if r.order_id in orders else ""), store_id=(orders.get(r.order_id).store_id if r.order_id in orders else "")) for r in reviews])


@router.get("")
def list_reviews(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """商家查看全部评价（含用户名/订单号/评分/内容）"""
    _require_merchant(user)
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    user_map = {u.id: u.username for u in db.query(User).all()}
    order_map = {o.id: o for o in db.query(Order).all()}
    out = []
    for r in reviews:
        o = order_map.get(r.order_id)
        out.append(_to_out(r, username=user_map.get(r.user_id, ""), order_no=o.order_no if o else "", store_id=o.store_id if o else ""))
    return ok(out)
