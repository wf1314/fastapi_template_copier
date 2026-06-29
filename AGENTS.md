# Repository Guidelines

## 仓库定位

本仓库是 Copier 模板，不是可直接部署的业务服务。`copier.yml` 定义生成参数，
`template/` 保存新项目内容，`tests/` 验证模板渲染结果。业务功能应在生成后的项目
中开发，不应加入模板仓库。

## 开发命令

- `uv sync`：安装 Copier 和模板测试依赖。
- `uv run pytest`：渲染模板，并在渲染产物内执行 `uv run ruff check`、`uv run mypy`、`uv run pytest`。
- `uv run copier copy . /tmp/example --defaults --trust`：手动生成默认项目。
- `uv run pre-commit run --all-files`：执行格式化和文件检查。

## 模板约定

- 所有生成项目文件放在 `template/` 下。
- 需要变量替换的文件使用 `.jinja` 后缀。
- 模板仓库测试不写只断言文件存在或字符串存在的单元式用例；新增模板行为时，优先通过“渲染到临时目录 → 在渲染产物中运行 ruff/mypy/pytest”的端到端质量闸覆盖。
- 新增模板问题时，端到端测试应覆盖默认值；涉及变量替换、包名、端口等参数时，同时覆盖自定义值。
- 保持模板为通用 FastAPI 基线，不加入具体行业、客户或智能体能力。
- 模板生成的数据库模型禁止声明数据库外键约束。
- Alembic 迁移版本只能在生成项目后通过 `alembic revision --autogenerate`
  创建，模板中不预置或手写版本文件。

## 提交规范

使用 Conventional Commits，例如 `feat:`、`fix:`、`docs:`、`test:`、
`refactor:`、`chore:`。
