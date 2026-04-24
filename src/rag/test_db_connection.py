from .db_config import get_db
from sqlalchemy import text

# 测试数据库连接
def test_db_connection():
    try:
        db = next(get_db())
        # 执行一个简单的查询
        result = db.execute(text("SELECT 1"))
        print("数据库连接成功！")
        print(f"查询结果: {result.fetchone()}")
        return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
