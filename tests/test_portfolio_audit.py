import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_portfolio import audit_portfolio  # noqa: E402


def test_real_portfolio_passes_strong_audit():
    assert audit_portfolio(ROOT) == []


@pytest.mark.parametrize(
    "field,value",
    [
        ("repo_url", "javascript:alert(1)"),
        ("repo_url", "https://evil.example/project"),
        ("demo_url", "data:text/html,bad"),
        ("demo_url", "../../secret"),
        ("demo_url", "https://evil.example/demo"),
    ],
)
def test_audit_rejects_unsafe_or_foreign_urls(tmp_path: Path, field: str, value: str):
    projects = json.loads((ROOT / "assets/data/projects.json").read_text(encoding="utf-8"))
    projects[0][field] = value
    _write_site(tmp_path, projects)

    assert any(field in error for error in audit_portfolio(tmp_path))


def test_audit_rejects_duplicate_ids_and_names(tmp_path: Path):
    projects = json.loads((ROOT / "assets/data/projects.json").read_text(encoding="utf-8"))
    projects[1]["id"] = projects[0]["id"]
    projects[2]["name"] = projects[0]["name"]
    _write_site(tmp_path, projects)

    errors = audit_portfolio(tmp_path)
    assert "projects.json: duplicate id" in errors
    assert "projects.json: duplicate name" in errors


def _write_site(root: Path, projects: list[dict]):
    (root / "assets/data").mkdir(parents=True)
    (root / "assets/data/projects.json").write_text(json.dumps(projects), encoding="utf-8")
    (root / "index.html").write_text('<link href="assets/css/main.css"><script src="assets/js/main.js"></script>', encoding="utf-8")
    (root / "assets/css").mkdir(parents=True)
    (root / "assets/js").mkdir(parents=True)
    (root / "assets/css/main.css").write_text("", encoding="utf-8")
    (root / "assets/js/main.js").write_text("", encoding="utf-8")
