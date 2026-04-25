#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORIES_DIR = ROOT / "truyen"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate chapters.json files for story folders."
    )
    parser.add_argument(
        "stories",
        nargs="*",
        type=Path,
        help="Optional story folders. Defaults to every subfolder in truyen/.",
    )
    parser.add_argument(
        "--stories-dir",
        type=Path,
        default=DEFAULT_STORIES_DIR,
        help="Parent folder containing story folders. Default: truyen/.",
    )
    args = parser.parse_args()

    story_dirs = args.stories or discover_story_dirs(resolve_path(args.stories_dir))
    if not story_dirs:
        print("No story folders found.")
        return 1

    for story_dir in story_dirs:
        story_dir = resolve_path(story_dir)
        manifest_path = story_dir / "chapters.json"
        manifest = build_manifest(story_dir, manifest_path)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"{relative(manifest_path)}: {len(manifest['chapters'])} chapters")

    return 0


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def discover_story_dirs(stories_dir: Path) -> list[Path]:
    if not stories_dir.exists():
        return []
    return sorted(path for path in stories_dir.iterdir() if path.is_dir())


def build_manifest(story_dir: Path, manifest_path: Path) -> dict[str, object]:
    existing = read_existing_manifest(manifest_path)
    title = existing.get("title") or title_from_slug(story_dir.name)

    chapters = []
    for chapter_path in sorted(story_dir.glob("*.md"), key=chapter_sort_key):
        chapters.append(
            {
                "name": chapter_path.name,
                "title": extract_title(chapter_path) or fallback_chapter_title(chapter_path),
            }
        )

    return {"title": title, "chapters": chapters}


def read_existing_manifest(manifest_path: Path) -> dict[str, object]:
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def chapter_sort_key(path: Path) -> tuple[list[int], str]:
    numbers = [int(value) for value in re.findall(r"\d+", path.stem)]
    return numbers or [10**9], path.name


def extract_title(path: Path) -> str:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
            bold_title = re.fullmatch(r"\*\*(.+?)\*\*", stripped)
            if bold_title:
                return bold_title.group(1).strip()
    return ""


def fallback_chapter_title(path: Path) -> str:
    numbers = re.findall(r"\d+", path.stem)
    if len(numbers) == 1:
        return f"Chương {numbers[0]}"
    if len(numbers) > 1:
        return f"Chương {'-'.join(numbers)}"
    return path.stem.replace("_", " ").replace("-", " ").title()


def title_from_slug(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
