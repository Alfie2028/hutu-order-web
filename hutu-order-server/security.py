"""安全模块：bcrypt 密码哈希 + JWT 签发/解析"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_DAYS


def hash_password(password: str) -> str:
    """bcrypt 加盐哈希，不可逆"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """校验明文密码与哈希是否匹配"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_token(user_id: int, username: str, role: str) -> str:
    """签发 JWT，携带 user_id / username / role，7 天过期"""
    expire = datetime.now(timezone.utc) + timedelta(days=JWT_EXPIRE_DAYS)
    payload = {"user_id": user_id, "username": username, "role": role, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """解析并校验 JWT，无效或过期抛异常"""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
