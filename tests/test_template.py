from pathlib import Path

import yaml
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).parents[1]


def render_project(destination: Path, **data: object) -> Path:
    run_copy(
        src_path=str(TEMPLATE_ROOT),
        dst_path=destination,
        data=data,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return destination


def test_copier_configuration_has_expected_questions() -> None:
    config = yaml.safe_load((TEMPLATE_ROOT / "copier.yml").read_text())

    assert config["_subdirectory"] == "template"
    assert config["_answers_file"] == ".copier-answers.yml"
    assert {
        "project_name",
        "project_slug",
        "package_name",
        "project_description",
        "author_name",
        "python_version",
        "timezone",
        "server_port",
    } <= config.keys()


def test_default_template_renders_without_business_features(tmp_path: Path) -> None:
    destination = render_project(tmp_path / "generated")

    assert (destination / "app" / "main.py").is_file()
    assert (destination / ".env.example").is_file()
    assert (destination / ".gitignore").is_file()
    assert (destination / ".copier-answers.yml").is_file()
    assert (destination / "alembic" / "versions" / ".gitkeep").is_file()
    assert (destination / "tests" / "test_logging.py").is_file()

    rendered_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in destination.rglob("*")
        if path.is_file()
    ).lower()
    for forbidden in (
        "deepagents",
        "langgraph",
        "agent/chat",
        "openai_api_key",
    ):
        assert forbidden not in rendered_text


def test_custom_answers_render_project_metadata(tmp_path: Path) -> None:
    destination = render_project(
        tmp_path / "custom",
        project_name="Orders API",
        project_slug="orders-api",
        package_name="orders_api",
        project_description="Order management backend",
        author_name="Platform Team",
        python_version="3.12",
        timezone="UTC",
        server_port=9000,
    )

    pyproject = (destination / "pyproject.toml").read_text()
    app_main = (destination / "orders_api" / "main.py").read_text()
    env_example = (destination / ".env.example").read_text()

    assert 'name = "orders-api"' in pyproject
    assert 'requires-python = ">=3.12"' in pyproject
    assert 'description="Order management backend"' in app_main
    assert "SERVER_PORT=9000" in env_example
    assert "TIMEZONE=UTC" in env_example
    assert "LOG_FORMAT=auto" in env_example
    assert "LOG_FILE_ENABLED=false" in env_example
