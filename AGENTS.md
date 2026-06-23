# Repository Guidelines

## 仓库定位

本仓库是 Copier 模板，不是可直接部署的业务服务。`copier.yml` 定义生成参数，
`template/` 保存新项目内容，`tests/` 验证模板渲染结果。业务功能应在生成后的项目
中开发，不应加入模板仓库。

## 开发命令

- `uv sync`：安装 Copier 和模板测试依赖。
- `uv run pytest`：渲染模板并检查生成结果。
- `uv run copier copy . /tmp/example --defaults --trust`：手动生成默认项目。
- `uv run pre-commit run --all-files`：执行格式化和文件检查。

## 模板约定

- 所有生成项目文件放在 `template/` 下。
- 需要变量替换的文件使用 `.jinja` 后缀。
- 新增模板问题时，同时覆盖默认值和自定义值测试。
- 保持模板为通用 FastAPI 基线，不加入具体行业、客户或智能体能力。
- 模板生成的数据库模型禁止声明数据库外键约束。
- Alembic 迁移版本只能在生成项目后通过 `alembic revision --autogenerate`
  创建，模板中不预置或手写版本文件。

## 提交规范

使用 Conventional Commits，例如 `feat:`、`fix:`、`docs:`、`test:`、
`refactor:`、`chore:`。
