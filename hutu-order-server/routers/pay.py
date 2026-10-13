"""支付接口：BufPay 真实接入（预留）+ 模拟支付"""
import hashlib
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from config import BUFPAY_AID, BUFPAY_SECRET, BUFPAY_PAY_URL
from database import get_db
from deps import get_current_user
from models import Order, Payment, Product, User
from utils import ok

router = APIRouter(prefix="/api/pay", tags=["支付"])


def bufpay_sign(*parts) -> str:
    """BufPay 签名：参数 value 顺序拼接后 MD5 小写"""
    return hashlib.md5("".join(parts).encode("utf-8")).hexdigest().lower()


def mark_order_paid(db: Session, order: Order, aoid: str = "", pay_type: str = ""):
    """订单置为已支付，累加销量，写支付记录（幂等由调用方保证）"""
    order.status = "paid"
    order.status_text = "已支付"
    order.paid_at = datetime.now(timezone.utc).replace(tzinfo=None)
    for item in order.items:
        product = db.get(Product, item.product_id)
        if product:
            product.sales += item.quantity
    db.add(Payment(order_id=order.id, aoid=aoid, pay_type=pay_type,
                   amount_cents=order.total_cents, status="paid"))
    db.commit()


def bufpay_create_order(order: Order, pay_type: str, notify_url: str) -> dict:
    """真实 BufPay 下单：MD5 签名后 POST，返回 JSON（含 qr_img / aoid）"""
    name = "校园点餐订单"
    price = f"{order.total_cents / 100:.2f}"
    order_id = order.order_no
    order_uid = str(order.user_id)
    return_url = ""
    feedback_url = ""
    sign = bufpay_sign(name, pay_type, price, order_id, order_uid,
                       notify_url, return_url, feedback_url, BUFPAY_SECRET)
    url = BUFPAY_PAY_URL.format(aid=BUFPAY_AID) + "?format=json"
    resp = httpx.post(url, data={
        "name": name, "pay_type": pay_type, "price": price,
        "order_id": order_id, "order_uid": order_uid,
        "notify_url": notify_url, "return_url": return_url,
        "feedback_url": feedback_url, "sign": sign,
    }, timeout=10.0)
    resp.raise_for_status()
    return resp.json()


@router.post("/orders/{order_id}/pay")
def create_payment(order_id: int, pay_type: str = "wechat",
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """发起支付：配置了 BufPay 密钥则真实下单，否则模拟支付（点击即成功）"""
    order = db.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail=f"订单状态为「{order.status_text}」，无需重复支付")

    if BUFPAY_AID and BUFPAY_SECRET:
        # notify_url 需替换为可公网访问的地址（内网穿透后）
        notify_url = "http://localhost:8000/api/pay/notify"
        try:
            data = bufpay_create_order(order, pay_type, notify_url)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"支付下单失败: {e}")
        return ok({"mode": "bufpay", "paid": False,
                   "qr_img": data.get("qr_img", ""), "pay_url": data.get("return_url", ""),
                   "aoid": data.get("aoid", "")})

    # 模拟支付：点击即成功
    mark_order_paid(db, order, aoid="", pay_type="mock")
    return ok({"mode": "mock", "paid": True, "qr_img": "", "pay_url": "", "aoid": ""})


@router.post("/notify")
async def pay_notify(request: Request, db: Session = Depends(get_db)):
    """BufPay 异步回调：验签 + 幂等 + 更新订单状态"""
    form = await request.form()
    sign = bufpay_sign(
        form.get("aoid", ""), form.get("order_id", ""), form.get("order_uid", ""),
        form.get("price", ""), form.get("pay_price", ""), BUFPAY_SECRET,
    )
    if sign != form.get("sign", ""):
        return {"status": "fail", "msg": "sign_error"}

    order = db.query(Order).filter(Order.order_no == form.get("order_id", "")).first()
    if not order:
        return {"status": "fail", "msg": "order_not_found"}
    if order.status == "pending":
        mark_order_paid(db, order, aoid=form.get("aoid", ""), pay_type="mock")
    return {"status": "success"}
