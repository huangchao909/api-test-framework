"""全局配置管理 - 支持 yaml / env / 环境变量 三层覆盖"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJ_ROOT = Path(__file__).resolve().parent.parent


class Settings:
    """配置类，优先级: 环境变量 > .env > 默认值"""

    # ---------- 环境 ----------
    ENV: str = os.getenv("TEST_ENV", "test")

    # ---------- API ----------
    BASE_URL: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    API_PREFIX: str = os.getenv("API_PREFIX", "")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # ---------- 认证 ----------
    AUTH_TOKEN: str | None = os.getenv("AUTH_TOKEN")
    AUTH_USERNAME: str | None = os.getenv("AUTH_USERNAME")
    AUTH_PASSWORD: str | None = os.getenv("AUTH_PASSWORD")

    # ---------- Allure ----------
    ALLURE_REPORT_DIR: Path = PROJ_ROOT / "reports" / "allure-results"

    # ---------- 请求默认 Headers ----------
    DEFAULT_HEADERS: dict = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # ---------- 多环境映射 ----------
    ENV_MAP: dict[str, str] = {
        "dev": "https://dev-api.example.com",
        "test": "https://jsonplaceholder.typicode.com",
        "staging": "https://staging-api.example.com",
        "prod": "https://api.example.com",
    }

    def get_base_url(self) -> str:
        return self.ENV_MAP.get(self.ENV, self.BASE_URL)


settings = Settings()
