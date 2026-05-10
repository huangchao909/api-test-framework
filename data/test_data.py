"""测试数据 - 用数据类管理，便于复用和维护"""
from dataclasses import dataclass, field, asdict
from utils.helpers import random_str, random_int


# ========== JSONPlaceholder 示例 ==========

@dataclass
class PostData:
    """创建帖子"""
    title: str = "测试标题"
    body: str = "测试内容"
    userId: int = 1

    @classmethod
    def random(cls, **overrides):
        data = cls(title=f"title_{random_str()}", body=f"body_{random_str()}")
        return asdict(data) | overrides


@dataclass
class UpdatePostData:
    id: int = 1
    title: str = "更新后的标题"
    body: str = "更新后的内容"
    userId: int = 1

    def dict(self, **overrides):
        return asdict(self) | overrides


# ========== 用户相关 ==========

@dataclass
class CreateUserData:
    name: str = field(default_factory=lambda: f"user_{random_str()}")
    username: str = field(default_factory=lambda: f"u_{random_str()}")
    email: str = field(default_factory=lambda: f"{random_str()}@example.com")
    phone: str = "13800138000"
    website: str = "example.com"

    def dict(self, **overrides):
        return asdict(self) | overrides


# ========== 业务数据池 ==========

class DataPool:
    """管理测试中生成的动态数据，便于清理"""

    def __init__(self):
        self.created_ids: list[int | str] = []
        self.created_records: list[dict] = []

    def add(self, record: dict):
        self.created_records.append(record)

    def add_id(self, id_: int | str):
        self.created_ids.append(id_)

    def cleanup(self):
        self.created_ids.clear()
        self.created_records.clear()
