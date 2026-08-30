#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import pathlib
import re
import sys
import unicodedata

README_PATH = pathlib.Path("README.md")
TOC_START = "<!-- toc:start -->"
TOC_END = "<!-- toc:end -->"
DOC_TITLE = "openpilot/etc. on Toyota/Lexus/Subaru with TSK/ECU SECURITY KEY/SecOC"
SKIP_TITLES = {
    "Table of Contents",
    "Bounty Statuses",
    "Pictures of TSK'd and non-TSK'd Camera ECUs",
}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^(```|~~~)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
FOOTNOTE_RE = re.compile(r"\[\^[^\]]+\]")
HTML_TAG_RE = re.compile(r"<[^>]+>")
TOC_WITH_MARKERS_RE = re.compile(
    rf"{re.escape(TOC_START)}\n.*?\n{re.escape(TOC_END)}",
    re.DOTALL,
)


def _plain_heading(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+#+$", "", text).strip()
    text = IMAGE_RE.sub(lambda m: m.group(1), text)
    text = LINK_RE.sub(lambda m: m.group(1), text)
    text = INLINE_CODE_RE.sub(lambda m: m.group(1), text)
    text = FOOTNOTE_RE.sub("", text)
    text = HTML_TAG_RE.sub("", text)
    text = re.sub(r"[*_~]", "", text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _slugify(text: str, seen: dict[str, int]) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    chars: list[str] = []
    for ch in normalized.lower():
        category = unicodedata.category(ch)
        if ch in {" ", "-"}:
            chars.append(ch)
        elif category.startswith("L") or category.startswith("N"):
            chars.append(ch)
    slug = "".join(chars)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    count = seen.get(slug, 0)
    seen[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count}"


def _toc_depth(
    level: int,
    title: str,
    current_h1: str | None,
    current_h2: str | None,
) -> int | None:
    if title in SKIP_TITLES or title == "Table of Contents":
        return None
    if title == "Discords of Note":
        return 0
    if current_h1 == DOC_TITLE:
        if level == 1:
            return 0
        if level == 2:
            return 1
        if current_h2 == "Cars" and level == 3:
            return 2
        if current_h2 == "Cars" and level == 4:
            return 3
        return None
    if current_h1 == "Setup Guide":
        if level == 1:
            return 0
        if level == 2:
            return 1
        return None
    if current_h1 == "Forks":
        if level == 1:
            return 0
        return None
    if current_h1 == "Current History":
        if level == 1:
            return 0
        return None
    return None


def build_toc(readme_text: str) -> str:
    current_h1: str | None = None
    current_h2: str | None = None
    seen_slugs: dict[str, int] = {}
    items: list[tuple[int, str, str]] = []
    in_fence = False

    for line in readme_text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = _plain_heading(match.group(2))
        if level == 1:
            current_h1 = title
            current_h2 = None
        elif level == 2:
            current_h2 = title
        slug = _slugify(title, seen_slugs)
        depth = _toc_depth(level, title, current_h1, current_h2)
        if depth is None:
            continue
        items.append((depth, title, slug))

    lines = [f"{'   ' * depth}* [{title}](#{slug})" for depth, title, slug in items]
    return "\n".join(lines)


def replace_toc_block(readme_text: str, toc_text: str) -> str:
    marked_block = f"{TOC_START}\n{toc_text}\n{TOC_END}"
    if TOC_START in readme_text and TOC_END in readme_text:
        return TOC_WITH_MARKERS_RE.sub(marked_block, readme_text, count=1)

    anchor = "## Table of Contents\n\n"
    separator = "\n---\n"
    if anchor not in readme_text:
        raise RuntimeError("Could not find '## Table of Contents' heading in README.md")
    start = readme_text.index(anchor) + len(anchor)
    end = readme_text.find(separator, start)
    if end == -1:
        raise RuntimeError("Could not find end of Table of Contents block in README.md")
    return readme_text[:start] + marked_block + readme_text[end:]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize the README table of contents."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of rewriting when the TOC is out of date.",
    )
    args = parser.parse_args()

    readme_text = README_PATH.read_text(encoding="utf-8")
    toc_text = build_toc(readme_text)
    updated_text = replace_toc_block(readme_text, toc_text)

    if args.check:
        if updated_text != readme_text:
            diff = difflib.unified_diff(
                readme_text.splitlines(),
                updated_text.splitlines(),
                fromfile="README.md",
                tofile="README.md (expected)",
                lineterm="",
            )
            for line in diff:
                print(line)
            print("README.md table of contents is out of date.", file=sys.stderr)
            return 1
        print("README.md table of contents is up to date.")
        return 0

    README_PATH.write_text(updated_text, encoding="utf-8")
    print("Synchronized README.md table of contents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
