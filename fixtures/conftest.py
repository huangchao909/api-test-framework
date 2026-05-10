"""Fixture 定义 - 作为 pytest 插件被 tests/conftest.py 加载"""
import pytest
from core.api_client import ApiClient
from data.test_data import DataPool


@pytest.fixture(scope="session")
def global_data_pool():
    """会话级别数据池，跨用例共享"""
    return DataPool()


@pytest.fixture(scope="function")
def function_data_pool():
    """函数级别数据池，每个用例独立"""
    return DataPool()


@pytest.fixture(scope="session")
def client() -> ApiClient:
    """全局共享的 API 客户端（会话级别）"""
    _client = ApiClient()
    yield _client
    _client.close()


@pytest.fixture(scope="function")
def anonymous_client() -> ApiClient:
    """匿名客户端（无 token），每个用例独立"""
    _client = ApiClient()
    _client.session.headers.pop("Authorization", None)
    yield _client
    _client.close()


@pytest.fixture(scope="function")
def logged_in_client(client) -> ApiClient:
    """登录后的客户端 - 可在此拓展 token 刷新逻辑"""
    yield client


@pytest.fixture(autouse=True)
def attach_environment_info(request):
    """在每个用例开始时，将环境信息附到 Allure 报告"""
    import allure
    from config.settings import settings
    allure.dynamic.environment(environment="测试环境", env=settings.ENV)
    allure.dynamic.feature(request.node.get_closest_marker("feature", None) or "")
