"""帖子 API 测试 - 以 JSONPlaceholder 为演示目标"""
import allure
import pytest

from core.assertions import ApiAssertions as Assert
from data.test_data import PostData, UpdatePostData

# 标记整个模块的 feature
pytestmark = [
    allure.feature("帖子管理"),
    pytest.mark.regression,
]

_POSTS = "/posts"


class TestPostsCRUD:

    @allure.story("查询帖子")
    @allure.title("获取所有帖子 - 返回列表且状态码 200")
    @pytest.mark.smoke
    @pytest.mark.get
    def test_get_all_posts(self, client):
        resp = client.get(_POSTS)
        Assert.status_code(resp, 200)
        Assert.list_length(resp, "", 100)

    @allure.story("查询帖子")
    @allure.title("获取单个帖子 - 验证字段完整性")
    @pytest.mark.p0
    @pytest.mark.get
    def test_get_post_by_id(self, client):
        resp = client.get(f"{_POSTS}/1")
        Assert.status_code(resp, 200)
        Assert.json_has_key(resp, "id")
        Assert.json_has_key(resp, "title")
        Assert.json_has_key(resp, "body")
        Assert.json_has_key(resp, "userId")
        Assert.json_equal(resp, "id", 1)

    @allure.story("查询帖子")
    @allure.title("获取不存在的帖子 - 返回 404")
    @pytest.mark.get
    def test_get_post_not_found(self, client):
        resp = client.get(f"{_POSTS}/99999")
        Assert.status_code(resp, 404)

    @allure.story("创建帖子")
    @allure.title("创建帖子 - 返回创建数据且状态码 201")
    @pytest.mark.smoke
    @pytest.mark.p0
    @pytest.mark.post
    def test_create_post(self, client, function_data_pool):
        body = PostData.random()
        resp = client.post(_POSTS, json=body)
        Assert.status_code(resp, 201)
        Assert.json_has_key(resp, "id")
        Assert.json_equal(resp, "title", body["title"])
        Assert.json_equal(resp, "body", body["body"])

        # 记录创建的 ID
        created_id = resp.json().get("id")
        if created_id:
            function_data_pool.add_id(created_id)

    @allure.story("创建帖子")
    @allure.title("创建帖子时传入空 body - 依然可以创建")
    @pytest.mark.post
    def test_create_post_empty_body(self, client):
        resp = client.post(_POSTS, json={})
        Assert.status_code(resp, 201)
        Assert.json_has_key(resp, "id")

    @allure.story("更新帖子")
    @allure.title("更新帖子 - 返回更新后的数据")
    @pytest.mark.p0
    @pytest.mark.put
    def test_update_post(self, client):
        body = UpdatePostData(id=1).dict()
        resp = client.put(f"{_POSTS}/1", json=body)
        Assert.status_code(resp, 200)
        Assert.json_equal(resp, "title", body["title"])
        Assert.json_equal(resp, "body", body["body"])

    @allure.story("更新帖子")
    @allure.title("部分更新帖子 - 仅修改 title")
    @pytest.mark.patch
    def test_patch_post(self, client):
        resp = client.patch(f"{_POSTS}/1", json={"title": "patched_title"})
        Assert.status_code(resp, 200)
        Assert.json_equal(resp, "title", "patched_title")

    @allure.story("删除帖子")
    @allure.title("删除帖子 - 返回空响应，状态码 200")
    @pytest.mark.p0
    @pytest.mark.delete
    def test_delete_post(self, client):
        resp = client.delete(f"{_POSTS}/1")
        Assert.status_code(resp, 200)

    @allure.story("查询帖子")
    @allure.title("按 userId 过滤帖子 - 返回对应用户的帖子")
    @pytest.mark.get
    def test_filter_posts_by_user(self, client):
        resp = client.get(_POSTS, params={"userId": 1})
        Assert.status_code(resp, 200)
        body = resp.json()
        assert all(item["userId"] == 1 for item in body), "返回结果中存在非 userId=1 的记录"

    @allure.story("性能")
    @allure.title("获取帖子响应时间小于 2s")
    @pytest.mark.p2
    def test_response_time(self, client):
        resp = client.get(f"{_POSTS}/1")
        Assert.response_time_lt(resp, 2000)
