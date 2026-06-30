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

## 模板开发

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
```

模板问题定义在 `copier.yml`，生成内容位于 `template/`。修改模板后应运行测试，
确认默认参数和自定义参数都能成功渲染。
