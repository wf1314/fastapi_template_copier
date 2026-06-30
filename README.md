# FastAPI Service Copier Template

这是一个纯 Copier 模板仓库，用于生成新的 FastAPI 后端项目。仓库本身不运行
业务服务，也不包含认证、智能体、MCP、模型调用或任何具体业务代码。

## 生成项目

推荐直接使用 `uvx`，无需在全局安装 Copier。模板托管在 GitHub，可直接从
远程仓库生成（`gh:` 是 Copier 对 GitHub 的内置简写）：

```bash
uvx copier copy gh:wf1314/fastapi_template_copier /path/to/new-project
```

或使用完整 HTTPS 地址：

```bash
uvx copier copy https://github.com/wf1314/fastapi_template_copier.git /path/to/new-project
```

生成项目会保存 `.copier-answers.yml`。模板发布新版本后，可在生成项目中执行：

```bash
uvx copier update
```

非交互生成：

```bash
uvx copier copy gh:wf1314/fastapi_template_copier /path/to/new-project \
  --defaults \
  --data project_name="Example Service" \
  --data project_slug="example-service" \
  --data package_name="example_service"
```

生成结果包含：

- 默认使用 `app/` 作为 Python 导入包目录
- FastAPI 应用工厂与 `/livez`、`/readyz` 健康检查
- `api/v1/<resource>/router.py` 和 `schema.py` 风格的接口模块
- 统一响应封装（`code/message/data/errors`）、通用错误码与全局异常处理
- 通用分页、排序请求参数依赖
- Loguru 日志，接管标准库与 Uvicorn 日志，并预置请求 ID、链路 ID 和耗时日志
- Pydantic Settings 环境配置
- SQLAlchemy 异步会话、PostgreSQL/MySQL URL 兼容、连接池参数、显式事务 helper 与空模型基类
- Alembic 迁移环境，不预置迁移版本
- 不绑定供应商的认证主体和权限依赖扩展点
- 可关闭的 Swagger、ReDoc 和 OpenAPI JSON
- `uv`、Ruff、mypy、pytest、pre-commit
- Dockerfile 与 `.dockerignore`
- 面向生成项目的 `AGENTS.md`

## 生成项目结构

以默认参数（包目录 `app/`）为例，生成的项目结构如下：

```
new-project/
├── app/                              # 导入包目录（package_name，默认 app/）
│   ├── api/
│   │   ├── health.py                 # /livez、/readyz 健康检查
│   │   └── v1/
│   │       ├── router.py             # v1 路由聚合
│   │       └── examples/             # 示例资源模块（router.py + schema.py）
│   ├── core/
│   │   ├── config.py                 # Pydantic Settings 环境配置
│   │   ├── exception/                # 异常、错误码、全局处理器
│   │   ├── middleware/request_context.py  # 请求 ID / 链路 ID 中间件
│   │   ├── logging.py                # Loguru 日志，接管标准库与 Uvicorn
│   │   ├── request_params.py         # 通用分页、排序依赖
│   │   ├── responses.py              # 统一响应封装（code/message/data/errors）
│   │   └── security.py               # 认证主体与权限依赖扩展点
│   ├── db/
│   │   ├── session.py                # SQLAlchemy 异步会话、连接池
│   │   └── transaction.py            # 显式事务 helper
│   ├── models/base.py                # 空模型基类，留作扩展
│   └── main.py                       # 应用工厂 create_app()
├── alembic/                          # 迁移环境（不预置迁移版本）
│   ├── env.py
│   └── versions/
├── tests/                            # 开箱即用的 pytest 测试
├── main.py                           # `uv run python main.py` 启动入口
├── pyproject.toml                    # uv、Ruff、mypy、pytest 配置
├── Dockerfile
├── Makefile
├── .env.example
└── AGENTS.md
```

`app/` 为默认包名；若在生成时指定其它 `package_name`，上述 `app/` 与
`app.main:app` 会相应替换。新增资源接口推荐沿用 `api/v1/<resource>/` 下
`router.py` + `schema.py` 的模块风格。

## 模板开发

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
```

模板问题定义在 `copier.yml`，生成内容位于 `template/`。修改模板后应运行测试，
确认默认参数和自定义参数都能成功渲染。
