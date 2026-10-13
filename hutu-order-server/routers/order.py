"""订单接口：下单 / 列表 / 详情 / 状态流转"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Coupon, Order, OrderItem, Product, Stall, Store, User
from schemas import OrderCreate, OrderOut
from utils import ok

router = APIRouter(prefix="/api/orders", tags=["订单"])

# 状态机操作分布：
#   用户：下单(pending) -> 支付(paid) -> 确认取餐(completed)
#   商家：接单(paid->making) -> 出餐(making->ready)，见 routers/merchant.py


def _gen_order_no() -> str:
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return f"XC{now:%Y%m%d}{int(now.timestamp() * 1000) % 1000000:06d}"


def _gen_pickup_code(db: Session, stall: Stall) -> str:
    """取餐码 = 档口编号(1位) + 当日序号(3位)，如 1023 = 1号档口当日第23单"""
    today = datetime.now(timezone.utc).replace(tzinfo=None).date()
    start = datetime.combine(today, datetime.min.time())
    count = db.query(Order).filter(Order.stall_id == stall.id, Order.created_at >= start).count()
    return f"{stall.code}{count + 1:03d}"


def _order_to_out(order: Order) -> dict:
    return OrderOut.model_validate(order).model_dump(mode="json")


@router.post("")
def create_order(body: OrderCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not body.items:
        raise HTTPException(status_code=400, detail="购物车为空")

    stall = db.get(Stall, body.stall_id)
    if not stall:
        raise HTTPException(status_code=400, detail="档口不存在")
    if not stall.is_active:
        raise HTTPException(status_code=400, detail="该档口已下架，请刷新菜单")

    if body.store_id:
        store = db.get(Store, body.store_id)
        if store and store.status == "closed":
            raise HTTPException(status_code=400, detail="店铺已打烊，暂无法下单")

    for it in body.items:
        prod = db.get(Product, it.product_id)
        if prod and not prod.is_active:
            raise HTTPException(status_code=400, detail=f"「{it.name}」已下架，请刷新菜单")

    subtotal = sum(it.unit_price_cents * it.quantity for it in body.items)
    discount = 0
    coupon_name = ""
    if body.coupon_id:
        coupon = db.query(Coupon).filter(Coupon.id == body.coupon_id, Coupon.is_active == True).first()
        if coupon and subtotal >= coupon.threshold_cents:
            discount = coupon.discount_cents
            coupon_name = coupon.name

    order = Order(
        order_no=_gen_order_no(),
        user_id=user.id,
        store_id=body.store_id,
        stall_id=body.stall_id,
        status="pending",
        status_text="待支付",
        pickup_code=_gen_pickup_code(db, stall),
        mode=body.mode,
        remark=body.remark,
        subtotal_cents=subtotal,
        discount_cents=discount,
        total_cents=max(0, subtotal - discount),
        coupon_name=coupon_name,
    )
    for it in body.items:
        order.items.append(OrderItem(
            product_id=it.product_id,
            name=it.name,
            quantity=it.quantity,
            unit_price_cents=it.unit_price_cents,
            options=it.options,
        ))
    db.add(order)
    db.commit()
    db.refresh(order)
    return ok(_order_to_out(order))


@router.get("")
def list_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
    return ok([_order_to_out(o) for o in orders])


@router.get("/{order_id}")
def get_order(order_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="订单不存在")
    return ok(_order_to_out(order))


@router.post("/{order_id}/complete")
def complete_order(order_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """用户确认取餐：ready -> completed"""
    order = db.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "ready":
        raise HTTPException(status_code=400, detail=f"订单状态为「{order.status_text}」，无法确认取餐")
    order.status, order.status_text = "completed", "已完成"
    db.commit()
    db.refresh(order)
    return ok(_order_to_out(order))
