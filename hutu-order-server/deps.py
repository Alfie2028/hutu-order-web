"""FastAPI 依赖：从请求头解析 JWT 得到当前用户"""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from security import decode_token


def get_current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    """解析 Authorization: Bearer <token>，返回当前 User；无 token 或过期则 401"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录或缺少 Token")
    token = authorization[7:]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")

    from models import User  # 延迟导入，避免循环依赖

    user = db.get(User, payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
