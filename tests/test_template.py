import os
import subprocess
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).parents[1]


def render_project(destination: Path, **data: object) -> Path:
    """用指定答案渲染 Copier 模板，返回生成项目路径。"""
    run_copy(
        src_path=str(TEMPLATE_ROOT),
        dst_path=destination,
        data=data,
        defaults=True,
        overwrite=True,
        unsafe=True,
    )
    return destination


def run_quality_gate(destination: Path) -> None:
    """在渲染产物中执行真实项目质量闸。"""
    env = os.environ.copy()
    env["UV_NO_PROGRESS"] = "1"

    for command in (
        ("uv", "run", "ruff", "check"),
        ("uv", "run", "mypy"),
        ("uv", "run", "pytest"),
    ):
        result = subprocess.run(
            command,
            cwd=destination,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"{' '.join(command)} failed in {destination}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


@pytest.mark.parametrize(
    ("name", "answers"),
    [
        ("default", {}),
        (
            "custom",
            {
                "project_name": "Orders API",
                "project_slug": "orders-api",
                "package_name": "orders_api",
                "project_description": "Order management backend",
                "author_name": "Platform Team",
                "python_version": "3.12",
                "server_port": 9000,
            },
        ),
    ],
)
def test_rendered_project_passes_quality_gate(
    tmp_path: Path,
    name: str,
    answers: dict[str, object],
) -> None:
    destination = render_project(tmp_path / name, **answers)

    run_quality_gate(destination)
