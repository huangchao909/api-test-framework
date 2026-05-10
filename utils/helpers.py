"""通用工具函数"""
import json
import random
import string
from pathlib import Path
from datetime import datetime


def random_str(length: int = 8) -> str:
    """生成随机字符串"""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_int(min_: int = 100, max_: int = 9999) -> int:
    return random.randint(min_, max_)


def load_json(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def deep_update(base: dict, update: dict) -> dict:
    """递归合并字典"""
    for k, v in update.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            deep_update(base[k], v)
        else:
            base[k] = v
    return base
