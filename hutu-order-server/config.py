"""全局配置：安全密钥、BufPay、数据库连接"""
import os

# ---- 安全 ----
JWT_SECRET = os.getenv("JWT_SECRET", "campus-order-dev-secret-change-in-prod")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 7

# ---- BufPay 聚合支付（免签模式，需安卓手机挂机监控到账）----
# aid / secret 在 BufPay 后台「应用配置」页查看；留空时支付自动走模拟
BUFPAY_AID = os.getenv("BUFPAY_AID", "")
BUFPAY_SECRET = os.getenv("BUFPAY_SECRET", "")
BUFPAY_PAY_URL = "https://bufpay.com/api/pay/{aid}"
BUFPAY_QUERY_URL = "https://bufpay.com/api/query/{aoid}"

# ---- 数据库 ----
DATABASE_URL = "sqlite:///./campus_order.db"
