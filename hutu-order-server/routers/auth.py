"""认证接口：注册 / 登录 / 头像"""
import base64

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import User
from schemas import UserLogin, UserOut, UserRegister, TokenOut
from security import create_token, hash_password, verify_password
from utils import ok

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(body: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少 6 位")

    user = User(username=body.username, password_hash=hash_password(body.password), role="user", points=0)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.username, user.role)
    return ok({"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(user).model_dump(mode="json")})


@router.post("/login")
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    token = create_token(user.id, user.username, user.role)
    return ok({"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(user).model_dump(mode="json")})


@router.post("/avatar")
def set_avatar(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """设置头像：上传图片，Base64 编码后存入数据库 User.avatar（不强制，可随时更换）"""
    data = file.file.read()
    b64 = base64.b64encode(data).decode("ascii")
    mime = file.content_type or "image/jpeg"
    user.avatar = f"data:{mime};base64,{b64}"
    db.commit()
    db.refresh(user)
    return ok(UserOut.model_validate(user).model_dump(mode="json"))
