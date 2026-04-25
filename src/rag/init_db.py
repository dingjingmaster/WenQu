from .db_config import engine, Base
from .models import Document

# 创建所有表
Base.metadata.create_all(bind=engine)
print("数据库表结构创建成功！")
