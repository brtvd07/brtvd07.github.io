import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

FIELDS = {"id", "name", "kind", "summary", "repo_url", "demo_url", "proof", "demo"}
IDS = {"skillary", "glowstudio", "nordmarket", "stroyraschet", "flowdesk", "telegram-freelance-agent", "telegram-expense-bot", "ai-support-bot", "booking-crm-bot"}
STAGING_DEMOS = {
    "../skillary/", "../glowstudio/", "../nordmarket/", "../stroyraschet/", "../flowdesk/",
    "../telegram-freelance-agent/README.md", "../telegram-expense-bot/README.md",
    "../ai-support-bot/demo/", "../booking-crm-bot/demo/",
}


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, _tag, attrs):
        values = dict(attrs)
        self.references.extend(values[key] for key in ("href", "src") if values.get(key))


def audit_portfolio(root: Path) -> list[str]:
    errors = []
    data_path = root / "assets/data/projects.json"
    try:
        projects = json.loads(data_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"projects.json: cannot read ({type(error).__name__})"]
    if not isinstance(projects, list) or len(projects) != 9:
        return ["projects.json: expected exactly 9 projects"]
    for index, project in enumerate(projects):
        prefix = f"projects.json[{index}]"
        if not isinstance(project, dict) or set(project) != FIELDS:
            errors.append(f"{prefix}: invalid schema")
            continue
        if project["id"] not in IDS:
            errors.append(f"{prefix}: invalid id")
        if project["kind"] not in {"web", "python"}:
            errors.append(f"{prefix}: invalid kind")
        if not all(isinstance(project[key], str) and project[key].strip() for key in ("name", "summary", "proof")):
            errors.append(f"{prefix}: empty text")
        if not isinstance(project["demo"], bool):
            errors.append(f"{prefix}: invalid demo")
        repo = urlparse(project["repo_url"])
        if (repo.scheme, repo.netloc, repo.path) != ("https", "github.com", f"/brtvd07/{project['id']}") or repo.params or repo.query or repo.fragment:
            errors.append(f"{prefix}: invalid repo_url")
        demo = project["demo_url"]
        parsed_demo = urlparse(demo)
        public_demo = (
            parsed_demo.scheme == "https"
            and not parsed_demo.username
            and not parsed_demo.password
            and not parsed_demo.port
            and (
                parsed_demo.netloc == "brtvd07.github.io"
                or (
                    parsed_demo.netloc == "github.com"
                    and parsed_demo.path.startswith("/brtvd07/")
                )
            )
        )
        if demo not in STAGING_DEMOS and not public_demo:
            errors.append(f"{prefix}: invalid demo_url")
        if demo in STAGING_DEMOS:
            target = (root / demo).resolve()
            package_root = root.parent.resolve()
            if package_root not in target.parents and target != package_root:
                errors.append(f"{prefix}: demo_url path traversal")
            elif not target.exists():
                errors.append(f"{prefix}: missing demo_url target")
            elif demo.endswith("/") and not (target / "index.html").is_file():
                errors.append(f"{prefix}: missing demo index.html")
    ids = [item.get("id") for item in projects if isinstance(item, dict)]
    names = [item.get("name") for item in projects if isinstance(item, dict)]
    if len(set(ids)) != len(ids):
        errors.append("projects.json: duplicate id")
    if len(set(names)) != len(names):
        errors.append("projects.json: duplicate name")
    for path in (root / "index.html", root / "assets/css/main.css", root / "assets/js/main.js", root / "assets/js/portfolio-state.js", data_path):
        if not path.is_file():
            errors.append(f"missing local asset: {path.relative_to(root)}")
    if (root / "index.html").is_file():
        parser = References()
        parser.feed((root / "index.html").read_text(encoding="utf-8"))
        for reference in parser.references:
            parsed = urlparse(reference)
            if parsed.scheme or reference.startswith(("#", "mailto:")):
                continue
            if not (root / parsed.path).is_file():
                errors.append(f"missing HTML target: {reference}")
    return errors


if __name__ == "__main__":
    import sys
    failures = audit_portfolio(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("."))
    if failures:
        print("\n".join(failures))
    raise SystemExit(bool(failures))
