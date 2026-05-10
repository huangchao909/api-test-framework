"""日志工具 - 基于 loguru"""
import sys
from pathlib import Path
from loguru import logger

_LOG_DIR = Path(__file__).resolve().parent.parent / "reports" / "logs"
_LOG_DIR.mkdir(parents=True, exist_ok=True)

# 移除默认 handler
logger.remove()

# 控制台输出
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{message}</cyan>",
    backtrace=False,
)

# 文件输出（保留全部级别用于排查）
logger.add(
    _LOG_DIR / "api_test_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="10 MB",
    retention=7,
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} | {message}",
)

api_logger = logger
