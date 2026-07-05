import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
INDEX = ROOT / "index.html"
PROJECTS = ROOT / "assets/data/projects.json"
SCRIPT = ROOT / "assets/js/main.js"
PROFILE = ROOT / "README.md"


def test_portfolio_has_exact_identity_contacts_and_working_resume_links():
    html = INDEX.read_text(encoding="utf-8")

    assert "Бритов Даниил" in html
    assert "https://github.com/brtvd07" in html
    assert 'href="https://t.me/brtvd_07"' in html
    assert 'href="mailto:danechkabritov@yandex.ru"' in html
    assert 'href="resume/daniil-britov-python-developer.pdf"' in html
    assert 'href="resume/daniil-britov-python-developer.docx"' in html
    assert "готовится" not in html.lower()
    assert (ROOT / "resume/daniil-britov-python-developer.pdf").is_file()
    assert (ROOT / "resume/daniil-britov-python-developer.docx").is_file()


def test_project_catalog_contains_exactly_nine_complete_truthful_records():
    projects = json.loads(PROJECTS.read_text(encoding="utf-8"))
    required = {
        "id", "name", "kind", "summary", "repo_url", "demo_url", "proof", "demo"
    }

    assert len(projects) == 9
    assert all(set(project) == required for project in projects)
    assert all(isinstance(project["demo"], bool) for project in projects)
    assert len({project["id"] for project in projects}) == 9
    assert len({project["name"] for project in projects}) == 9
    assert sum(project["kind"] == "web" for project in projects) == 5
    assert {project["name"] for project in projects} == {
        "Skillary", "GlowStudio", "NordMarket", "СтройРасчёт", "FlowDesk",
        "Telegram Freelance Agent", "Telegram Expense Bot", "AI Support Bot",
        "Booking CRM Bot",
    }
    assert all(project["repo_url"].startswith("https://github.com/brtvd07/") for project in projects)
    assert all(project["demo_url"] for project in projects)
    assert all(project["summary"] and project["proof"] for project in projects)


def test_catalog_is_loaded_by_javascript_and_filters_are_data_driven():
    script = SCRIPT.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")

    assert "assets/data/projects.json" in script
    assert "fetch(" in script
    assert "data-filter" in html
    assert 'data-filter="all"' in html
    assert 'data-filter="web"' in html
    assert 'data-filter="python"' in html
    assert "project.kind" in script


def test_portfolio_has_accessible_navigation_and_no_unsupported_claims():
    public_text = "\n".join(
        [
            INDEX.read_text(encoding="utf-8"),
            PROJECTS.read_text(encoding="utf-8"),
            PROFILE.read_text(encoding="utf-8"),
        ]
    ).lower()
    html = INDEX.read_text(encoding="utf-8")

    assert 'aria-controls="site-nav"' in html
    assert 'aria-expanded="false"' in html
    assert "testimonial" not in public_text
    assert "отзывы" not in public_text
    assert "15+" not in public_text
    assert "лет опыта" not in public_text
    assert "наши клиенты" not in public_text
    assert "форма успешно" not in public_text
    assert "все репозитории доступны" not in public_text
    assert "каждый публичный кейс можно открыть" not in public_text


def test_profile_readme_has_positioning_contacts_stack_and_six_featured_projects():
    profile = PROFILE.read_text(encoding="utf-8")

    assert "Бритов Даниил" in profile
    assert "Python" in profile
    assert "Telegram" in profile
    assert "FastAPI" in profile
    assert "https://brtvd07.github.io" in profile
    assert "https://t.me/brtvd_07" in profile
    assert "mailto:danechkabritov@yandex.ru" in profile
    assert "Открыт к новым проектам" in profile
    assert profile.count("<!-- featured-project -->") == 6
    assert "visitor" not in profile.lower()
    assert "%" not in profile


def test_pages_workflow_runs_checks_before_deployment():
    workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")

    assert "needs: test" in workflow
    assert "pytest" in workflow
    assert "check_static_site.py" in workflow
    assert "node --check assets/js/main.js" in workflow
    assert "audit_portfolio.py" in workflow
    assert "node --test tests/portfolio-state.test.js" in workflow
    assert "actions/upload-pages-artifact@v3" in workflow
    assert "actions/deploy-pages@v4" in workflow


def test_portfolio_has_honest_search_metadata():
    html = INDEX.read_text(encoding="utf-8")

    assert '<link rel="canonical" href="https://brtvd07.github.io/">' in html
    assert '<meta name="robots" content="index, follow">' in html
    assert '"@type":"Person"' in html
    assert '"name":"Бритов Даниил"' in html


def test_pages_checker_is_packaged_with_the_site():
    assert (ROOT / "scripts/check_static_site.py").is_file()
    assert (ROOT / "scripts/audit_portfolio.py").is_file()
