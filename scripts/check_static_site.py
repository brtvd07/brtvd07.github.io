import argparse
from html.parser import HTMLParser
from pathlib import Path


class PortfolioParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang_ru = self.viewport = self.description = self.telegram = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.lang_ru |= tag == "html" and values.get("lang", "").lower() == "ru"
        self.viewport |= tag == "meta" and values.get("name", "").lower() == "viewport"
        self.description |= tag == "meta" and values.get("name", "").lower() == "description" and bool(values.get("content", "").strip())
        self.telegram |= tag == "a" and values.get("href") == "https://t.me/brtvd_07"


def check_site(root: Path) -> list[str]:
    index = root / "index.html"
    if not index.is_file():
        return ["missing index.html"]
    parser = PortfolioParser()
    parser.feed(index.read_text(encoding="utf-8"))
    checks = (
        (parser.lang_ru, "index.html: missing lang=ru"),
        (parser.viewport, "index.html: missing viewport"),
        (parser.description, "index.html: missing description"),
        (parser.telegram, "index.html: missing Telegram contact"),
        ((root / "assets/css/main.css").is_file(), "missing assets/css/main.css"),
        ((root / "assets/js/main.js").is_file(), "missing assets/js/main.js"),
    )
    return [message for valid, message in checks if not valid]


def main() -> int:
    arguments = argparse.ArgumentParser()
    arguments.add_argument("site_dir", nargs="?", type=Path, default=Path("."))
    arguments.add_argument("--portfolio", action="store_true")
    errors = check_site(arguments.parse_args().site_dir)
    if errors:
        print("\n".join(errors))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
