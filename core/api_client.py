"""核心 API 客户端 - 封装 requests，支持重试、日志、Allure 报告"""
import time
import json as json_lib

import allure
import requests
from requests import Response, Session, adapters

from config.settings import settings
from utils.logger import api_logger


class ApiClient:
    """统一 HTTP 客户端"""

    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or settings.get_base_url()).rstrip("/")
        self.session = Session()
        self.session.headers.update(settings.DEFAULT_HEADERS)

        # 重试适配器
        retry_adapter = adapters.HTTPAdapter(
            max_retries=settings.MAX_RETRIES,
            pool_connections=10,
            pool_maxsize=20,
        )
        self.session.mount("http://", retry_adapter)
        self.session.mount("https://", retry_adapter)

        # 认证
        if settings.AUTH_TOKEN:
            self.session.headers["Authorization"] = f"Bearer {settings.AUTH_TOKEN}"
        if settings.AUTH_USERNAME and settings.AUTH_PASSWORD:
            self.session.auth = (settings.AUTH_USERNAME, settings.AUTH_PASSWORD)

    # ------------------------------------------------------------------
    # 请求方法
    # ------------------------------------------------------------------

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", settings.REQUEST_TIMEOUT)

        # ===== Allure 报告 - 请求信息 =====
        with allure.step(f"{method.upper()} {endpoint}"):
            allure.attach(
                url,
                name="请求 URL",
                attachment_type=allure.attachment_type.TEXT,
            )
            if "json" in kwargs:
                body = kwargs["json"]
                allure.attach(
                    json_lib.dumps(body, indent=2, ensure_ascii=False),
                    name="请求 Body",
                    attachment_type=allure.attachment_type.JSON,
                )
            if "params" in kwargs and kwargs["params"]:
                allure.attach(
                    json_lib.dumps(kwargs["params"], indent=2),
                    name="请求 Params",
                    attachment_type=allure.attachment_type.JSON,
                )
            if "headers" in kwargs and kwargs["headers"]:
                safe_headers = {
                    k: v for k, v in kwargs["headers"].items()
                    if "authorization" not in k.lower()
                }
                allure.attach(
                    json_lib.dumps(safe_headers, indent=2),
                    name="请求 Headers",
                    attachment_type=allure.attachment_type.JSON,
                )

        # 日志
        api_logger.info(f"{'─' * 60}")
        api_logger.info(f"[请求] {method.upper()} {url}")
        if "json" in kwargs:
            api_logger.debug(f"[Body] {json_lib.dumps(kwargs['json'], ensure_ascii=False)}")

        # 发送
        start = time.time()
        resp: Response = self.session.request(method, url, **kwargs)
        elapsed = round((time.time() - start) * 1000)

        # ===== Allure 报告 - 响应信息 =====
        with allure.step(f"响应 {resp.status_code} ({elapsed}ms)"):
            try:
                resp_body = resp.json()
                allure.attach(
                    json_lib.dumps(resp_body, indent=2, ensure_ascii=False),
                    name="响应 Body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    resp.text[:5000],
                    name="响应 Body（文本）",
                    attachment_type=allure.attachment_type.TEXT,
                )

            # 响应头
            allure.attach(
                json_lib.dumps(dict(resp.headers), indent=2),
                name="响应 Headers",
                attachment_type=allure.attachment_type.JSON,
            )

        # 日志
        api_logger.info(f"[响应] {resp.status_code} ({elapsed}ms)")
        if resp.headers.get("content-type", "").startswith("application/json"):
            try:
                api_logger.debug(f"[Body] {json_lib.dumps(resp.json(), indent=2, ensure_ascii=False)}")
            except Exception:
                pass

        return resp

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self._request("DELETE", endpoint, **kwargs)

    # ------------------------------------------------------------------
    # 便捷方法
    # ------------------------------------------------------------------

    def get_json(self, endpoint: str, **kwargs) -> dict:
        resp = self.get(endpoint, **kwargs)
        return resp.json()

    def post_json(self, endpoint: str, **kwargs) -> dict:
        resp = self.post(endpoint, **kwargs)
        return resp.json()

    def close(self):
        self.session.close()
