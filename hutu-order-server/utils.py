"""统一响应格式辅助函数"""


def ok(data=None):
    """成功响应：{code:0, msg:'ok', data:...}"""
    return {"code": 0, "msg": "ok", "data": data}


def fail(msg="error", code=1):
    """失败响应：{code:非0, msg:..., data:None}"""
    return {"code": code, "msg": msg, "data": None}
