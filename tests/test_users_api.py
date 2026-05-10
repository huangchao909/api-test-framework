"""用户 API 测试 - 演示复杂断言和 Schema 校验"""
import allure
import pytest

from core.assertions import ApiAssertions as Assert

pytestmark = [
    allure.feature("用户管理"),
    pytest.mark.regression,
]

_USERS = "/users"

# 用户响应 JSON Schema
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode", "geo"],
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {"type": "object"},
    },
}


class TestUsers:

    @allure.story("查询用户")
    @allure.title("获取所有用户 - 返回列表")
    @pytest.mark.smoke
    @pytest.mark.get
    def test_get_all_users(self, client):
        resp = client.get(_USERS)
        Assert.status_code(resp, 200)
        assert len(resp.json()) > 0

    @allure.story("查询用户")
    @allure.title("获取单个用户 - 校验字段完整")
    @pytest.mark.p0
    @pytest.mark.get
    def test_get_user_by_id(self, client):
        resp = client.get(f"{_USERS}/1")
        Assert.status_code(resp, 200)
        Assert.json_equal(resp, "id", 1)
        Assert.json_has_key(resp, "name")
        Assert.json_has_key(resp, "address")
        Assert.json_has_key(resp, "company")

    @allure.story("查询用户")
    @allure.title("获取单个用户 - 校验 JSON Schema")
    @pytest.mark.p0
    @pytest.mark.get
    def test_user_schema(self, client):
        resp = client.get(f"{_USERS}/1")
        Assert.status_code(resp, 200)
        Assert.json_schema(resp, USER_SCHEMA)

    @allure.story("查询用户")
    @allure.title("用户邮箱格式校验")
    @pytest.mark.p1
    @pytest.mark.get
    def test_user_email_format(self, client):
        resp = client.get(f"{_USERS}/1")
        Assert.status_code(resp, 200)
        email = resp.json().get("email", "")
        assert "@" in email, f"邮箱格式不正确: {email}"

    @allure.story("查询用户")
    @allure.title("获取不存在的用户 - 返回空对象")
    @pytest.mark.get
    def test_get_user_not_found(self, client):
        resp = client.get(f"{_USERS}/99")
        Assert.status_code(resp, 200)
        body = resp.json()
        assert body == {}, f"不存在的用户应返回空对象，实际: {body}"

    @allure.story("查询用户")
    @allure.title("用户嵌套对象深度断言")
    @pytest.mark.p2
    @pytest.mark.get
    def test_user_nested_fields(self, client):
        resp = client.get(f"{_USERS}/1")
        body = resp.json()

        # 地址嵌套
        address = body.get("address", {})
        assert "city" in address, "地址缺少 city 字段"
        assert "geo" in address, "地址缺少 geo 字段"
        geo = address.get("geo", {})
        assert "lat" in geo, "geo 缺少 lat"
        assert "lng" in geo, "geo 缺少 lng"

        # 公司嵌套
        company = body.get("company", {})
        assert "name" in company, "公司缺少 name 字段"
        assert "catchPhrase" in company, "公司缺少 catchPhrase 字段"

    @allure.story("查询用户")
    @allure.title("response_time_lt 断言演示")
    @pytest.mark.p2
    def test_response_time_users(self, client):
        resp = client.get(_USERS)
        Assert.response_time_lt(resp, 3000)
