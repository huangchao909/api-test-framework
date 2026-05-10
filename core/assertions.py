"""自定义断言 - Allure 友好 + 详细 diff 输出"""
import json

import allure
from deepdiff import DeepDiff
from jsonschema import validate, ValidationError


class ApiAssertions:

    @staticmethod
    @allure.step("校验 HTTP 状态码")
    def status_code(resp, expected: int = 200):
        actual = resp.status_code
        assert actual == expected, (
            f"状态码不符: expected={expected}, actual={actual}\n"
            f"响应体: {resp.text[:500]}"
        )

    @staticmethod
    @allure.step("校验 JSON 响应包含字段")
    def json_has_key(resp, key: str):
        body = resp.json()
        assert key in body, (
            f"响应中缺少字段 '{key}'\n"
            f"可用字段: {list(body.keys())}"
        )

    @staticmethod
    @allure.step("校验 JSON 响应不包含字段")
    def json_not_has_key(resp, key: str):
        body = resp.json()
        assert key not in body, f"响应中不应包含字段 '{key}'"

    @staticmethod
    @allure.step("校验 JSON 字段值")
    def json_equal(resp, key: str, expected):
        body = resp.json()
        actual = body
        # 支持点号路径: data.user.name
        for part in key.split("."):
            if isinstance(actual, dict) and part in actual:
                actual = actual[part]
            else:
                raise AssertionError(f"路径 '{key}' 在响应中不存在: {body}")
        assert actual == expected, (
            f"字段 '{key}' 值不符:\n"
            f"  expected = {expected}\n"
            f"  actual   = {actual}"
        )

    @staticmethod
    @allure.step("校验整个 JSON 响应与预期一致")
    def json_match(resp, expected: dict, exclude_paths: list[str] | None = None):
        actual = resp.json() if hasattr(resp, "json") else resp
        diff = DeepDiff(actual, expected, exclude_paths=exclude_paths, verbose_level=2)
        assert not diff, (
            f"JSON 不匹配:\n{diff.to_json(indent=2)}"
        )

    @staticmethod
    @allure.step("校验 JSON Schema")
    def json_schema(resp, schema: dict):
        body = resp.json() if hasattr(resp, "json") else resp
        try:
            validate(body, schema)
        except ValidationError as e:
            allure.attach(
                json.dumps(schema, indent=2),
                name="Schema",
                attachment_type=allure.attachment_type.JSON,
            )
            raise AssertionError(f"Schema 校验失败: {e.message}") from e

    @staticmethod
    @allure.step("校验响应时间")
    def response_time_lt(resp, ms: int = 3000):
        assert resp.elapsed.microseconds / 1000 < ms, (
            f"响应时间超过 {ms}ms: {resp.elapsed.microseconds / 1000:.0f}ms"
        )

    @staticmethod
    @allure.step("校验列表长度")
    def list_length(resp, path: str, expected_len: int):
        body = resp.json()
        data = body
        for part in path.split("."):
            data = data.get(part, {}) if isinstance(data, dict) else data
        assert len(data) == expected_len, (
            f"列表 '{path}' 长度不符: expected={expected_len}, actual={len(data)}"
        )

    @staticmethod
    @allure.step("校验字段类型")
    def json_type(resp, key: str, expected_type: type):
        body = resp.json()
        actual = body
        for part in key.split("."):
            actual = actual.get(part) if isinstance(actual, dict) else actual
        assert isinstance(actual, expected_type), (
            f"字段 '{key}' 类型不符: expected={expected_type.__name__}, "
            f"actual={type(actual).__name__}, value={actual}"
        )
