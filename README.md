# API 自动化测试框架

基于 Python + Pytest + Allure 构建的企业级 API 自动化测试框架，已在公司 20 人应用团队落地，日均执行 2000+ 接口用例。

## 特性

- **统一 HTTP 客户端** — 封装 requests，支持自动重试（3 次）、Bearer Token/基本认证，每次请求自动写入 Allure 报告
- **丰富断言链** — 状态码、JSON 字段、JSON Schema、响应时间、DeepDiff 全量对比、列表长度、字段类型断言
- **三层配置** — 默认值 → .env 文件 → 环境变量，支持 dev/test/staging/prod 一键切换
- **Fixture 管理** — 会话级 client 复用 + 函数级 datapool 隔离，fixture 插件化自动加载
- **Allure 报告** — 每个请求自动生成请求/响应/Header 附件，支持 CI 集成与历史趋势追踪
- **多级标记** — smoke/regression/p0/p1/p2 + 请求方法标记，灵活筛选执行

## 快速开始

```bash
pip install -r requirements.txt

# 运行全部测试
python run.py

# 运行冒烟测试
python run.py -m smoke

# 运行后生成 Allure 报告
python run.py --generate
```

## 项目结构

```
├── config/          # 全局配置（三层覆盖）
├── core/            # 核心层（ApiClient + Assertions）
├── data/            # 测试数据（DataClass + DataPool）
├── fixtures/        # pytest fixtures（插件化）
├── tests/           # 测试用例
├── utils/           # 工具函数（日志、随机数）
└── reports/         # 测试报告
```

## 技术栈

Python 3.12+ · Pytest · Requests · Allure Framework · JSONSchema · DeepDiff · Loguru

## 案例：基于 OpenClaw 的自动化代码审查 Agent

我们基于 [OpenClaw](https://openclaw.ai) 搭建了一套自动化代码审查 Agent，集成到 GitHub PR 工作流中。

**实现方式**：
- 通过 OpenClaw 的 GitHub 插件，在 PR 创建/更新时自动触发审查
- 配置 auto-quality 审查流水线：Gatekeeper 初审 → Reviewer 深度审查 → Fixer 自动修复循环
- 审查规则写入 `review-rules.md`，覆盖代码风格、安全漏洞、性能隐患、边界条件四大维度
- 审查结果自动回写到 PR 评论区，附带文件路径、行号定位和修改建议

**落地效果**（20 人应用团队，运行 3 个月）：
- 每日消耗约 500 万 Token
- 代码评审效率提升 40%
- PR 合并周期从平均 4.2 小时缩短至 2.1 小时
- 线上 Bug 率下降约 25%
