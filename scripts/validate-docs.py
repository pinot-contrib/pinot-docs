#!/usr/bin/env python3
"""
Docs validation script for the Apache Pinot documentation site.

Checks:
  1. SUMMARY.md integrity  — every path in SUMMARY.md resolves to a real file.
  2. Broken file links     — markdown links, HTML hrefs, and GitBook
                              content-ref blocks that point to .md files
                              or directories that do not exist.
  3. Broken anchors        — links to #heading-anchors where the target
                              heading does not exist in the destination file.
                              (Warning only — GitBook generates anchors that
                              may not match standard slug rules.)
  4. Reachability          — every .md file is reachable from SUMMARY.md
                              or another docs page.
  5. Function family coverage — each functions/* page is linked from its
                                family README.md.
  6. Function SUMMARY coverage — each published functions/* page appears
                                 in SUMMARY.md.
  7. Redirect coverage     — .gitbook.yaml redirect targets that do not exist.
  8. Orphan file check     — every .md file on disk is listed in
                              SUMMARY.md (prevents undiscoverable pages).

Modes:
  Default (no flags)   — report everything, fail on broken file links,
                          SUMMARY.md issues, unlinked pages, missing
                          function-family links, missing function-summary
                          entries, and redirect issues.
  --strict             — also fail on broken anchors.
  --warn-only          — report everything but always exit 0.
  --summary-only       — print counts only, no per-file details.
  --changed-only=FILE  — only check files listed in FILE (one path per line).
                          Useful in CI to check only files changed in a PR.

Exit codes:
  0  all enforced checks pass (or --warn-only)
  1  one or more enforced checks failed
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
GITBOOK_YAML = REPO_ROOT / ".gitbook.yaml"
FUNCTIONS_ROOT = REPO_ROOT / "functions"

SKIP_DIRS = {".git", ".claude", "node_modules", ".gitbook"}
FUNCTION_FAMILY_LINK_EXCLUSIONS = set()

# Files that are intentionally NOT in SUMMARY.md (e.g. includes, internal pages)
SUMMARY_ORPHAN_EXCLUSIONS = {
    REPO_ROOT / "SUMMARY.md",
    REPO_ROOT / "README.md",  # Root readme is referenced by .gitbook.yaml, not SUMMARY.md
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify_heading(heading_text: str) -> str:
    """Convert a markdown heading to an anchor slug."""
    text = heading_text.strip().lower()
    # Remove markdown link syntax from heading: [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Remove inline code backticks
    text = text.replace("`", "")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def collect_headings(filepath: Path) -> set[str]:
    """Return the set of anchor slugs defined by headings in a markdown file."""
    headings = set()
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return headings
    for m in re.finditer(r"^#{1,6}\s+(.+)$", content, re.MULTILINE):
        headings.add(slugify_heading(m.group(1)))
    return headings


def all_md_files(root: Path) -> set[Path]:
    """Return every .md file under root, skipping SKIP_DIRS."""
    files = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                files.add(Path(dirpath) / fn)
    return files


# ---------------------------------------------------------------------------
# Link extraction
# ---------------------------------------------------------------------------

MD_LINK = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
HTML_HREF = re.compile(r'(?:href|url)=["\']([^"\']+)["\']')
CONTENT_REF_URL = re.compile(r'{%\s*content-ref\s+url=["\']([^"\']+)["\']')


def extract_links(filepath: Path) -> list[tuple[str, int]]:
    """
    Return (raw_link, line_number) for every internal link in the file.
    External links (http/https/mailto) are excluded.
    """
    links = []
    try:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return links

    for lineno, line in enumerate(lines, start=1):
        for pattern in (MD_LINK, HTML_HREF, CONTENT_REF_URL):
            for m in pattern.finditer(line):
                raw = m.group(1).strip()
                if raw.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if raw.startswith(("{%", "<")):
                    continue
                if raw.startswith("/wiki/"):
                    continue
                raw = re.sub(r'\s+"mention"\s*$', '', raw)
                links.append((raw, lineno))
    return links


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def resolve_link(source: Path, raw_link: str) -> tuple[Path | None, str | None]:
    """Resolve a raw link relative to the source file."""
    if "#" in raw_link:
        path_part, anchor = raw_link.split("#", 1)
    else:
        path_part, anchor = raw_link, None

    if not path_part:
        return source, anchor

    source_dir = source.parent
    resolved = (source_dir / path_part).resolve()

    if resolved.is_dir():
        readme = resolved / "README.md"
        if readme.exists():
            return readme, anchor
        return resolved, anchor

    return resolved, anchor


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_summary_targets() -> tuple[list[str], int]:
    """Verify every path in SUMMARY.md exists. Returns (errors, count)."""
    if not SUMMARY_PATH.exists():
        return (["SUMMARY.md not found"], 0)

    errors = []
    count = 0
    content = SUMMARY_PATH.read_text(encoding="utf-8", errors="replace")

    for lineno, line in enumerate(content.splitlines(), start=1):
        for m in MD_LINK.finditer(line):
            raw = m.group(1).strip()
            if raw.startswith(("http://", "https://", "#")):
                continue
            count += 1
            path_part = raw.split("#")[0] if "#" in raw else raw
            if not path_part:
                continue
            resolved = (REPO_ROOT / path_part).resolve()
            if resolved.is_dir():
                resolved = resolved / "README.md"
            if not resolved.exists():
                errors.append(f"  SUMMARY.md:{lineno}  →  {raw}")
    return errors, count


def check_broken_links(
    md_files: set[Path],
) -> tuple[list[str], list[str], int]:
    """
    Returns (file_errors, anchor_warnings, total_links_checked).
    file_errors:     links whose target file/dir does not exist.
    anchor_warnings: links where the file exists but the anchor is missing.
    """
    file_errors = []
    anchor_warnings = []
    total = 0
    heading_cache: dict[Path, set[str]] = {}

    for filepath in sorted(md_files):
        for raw_link, lineno in extract_links(filepath):
            resolved, anchor = resolve_link(filepath, raw_link)
            if resolved is None:
                continue
            total += 1

            rel_source = filepath.relative_to(REPO_ROOT)

            if not resolved.exists():
                try:
                    rel_target = resolved.relative_to(REPO_ROOT)
                except ValueError:
                    rel_target = resolved
                file_errors.append(
                    f"  {rel_source}:{lineno}  →  {raw_link}\n"
                    f"      target: {rel_target}"
                )
                continue

            if anchor and resolved.suffix == ".md":
                if resolved not in heading_cache:
                    heading_cache[resolved] = collect_headings(resolved)
                if anchor not in heading_cache[resolved]:
                    anchor_warnings.append(
                        f"  {rel_source}:{lineno}  →  {raw_link}\n"
                        f"      anchor #{anchor} not found in "
                        f"{resolved.relative_to(REPO_ROOT)}"
                    )
    return file_errors, anchor_warnings, total


def find_orphan_pages(md_files: set[Path]) -> list[Path]:
    """Find .md files not referenced from any other file."""
    referenced: set[Path] = set()

    for filepath in md_files:
        for raw_link, _ in extract_links(filepath):
            resolved, _ = resolve_link(filepath, raw_link)
            if resolved and resolved.exists():
                referenced.add(resolved.resolve())

    # Root pages are always reachable
    referenced.add((REPO_ROOT / "README.md").resolve())
    referenced.add(SUMMARY_PATH.resolve())

    orphans = []
    for filepath in sorted(md_files):
        if filepath.resolve() not in referenced:
            orphans.append(filepath)
    return orphans


def check_redirects() -> tuple[list[str], int]:
    """Verify redirect targets in .gitbook.yaml exist."""
    if not GITBOOK_YAML.exists():
        return [], 0

    try:
        with open(GITBOOK_YAML) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        return [f"  Could not parse .gitbook.yaml: {e}"], 0

    redirects = config.get("redirects", {})
    root_dir = config.get("root", "./")
    base = REPO_ROOT / root_dir
    errors = []

    for old_path, new_path in redirects.items():
        target = base / new_path
        if target.is_dir():
            target = target / "README.md"
        if not target.exists():
            errors.append(f"  {old_path}  →  {new_path}")

    return errors, len(redirects)


def check_function_family_links(
    changed_files: set[Path] | None = None,
) -> tuple[list[str], int]:
    """Verify each function page is linked from its family README."""
    if not FUNCTIONS_ROOT.exists():
        return [], 0

    errors = []
    total = 0

    for family_dir in sorted(FUNCTIONS_ROOT.iterdir()):
        if not family_dir.is_dir():
            continue

        readme = family_dir / "README.md"
        if not readme.exists():
            continue

        if changed_files is not None:
            relevant = any(
                changed == readme or changed.parent == family_dir
                for changed in changed_files
            )
            if not relevant:
                continue

        linked_pages: set[Path] = set()
        for raw_link, _ in extract_links(readme):
            resolved, _ = resolve_link(readme, raw_link)
            if resolved is None or not resolved.exists():
                continue
            if resolved.parent == family_dir and resolved.name != "README.md":
                linked_pages.add(resolved.resolve())

        for page in sorted(family_dir.glob("*.md")):
            if page.name == "README.md" or page in FUNCTION_FAMILY_LINK_EXCLUSIONS:
                continue
            total += 1
            if page.resolve() not in linked_pages:
                errors.append(
                    f"  {readme.relative_to(REPO_ROOT)} missing link to "
                    f"{page.relative_to(REPO_ROOT)}"
                )

    return errors, total


def check_function_summary_coverage() -> tuple[list[str], int]:
    """Verify each published function page is listed in SUMMARY.md."""
    if not FUNCTIONS_ROOT.exists() or not SUMMARY_PATH.exists():
        return [], 0

    summary_targets: set[Path] = set()
    for raw_link, _ in extract_links(SUMMARY_PATH):
        path_part = raw_link.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (REPO_ROOT / path_part).resolve()
        if resolved.exists():
            summary_targets.add(resolved)

    errors = []
    total = 0

    for page in sorted(FUNCTIONS_ROOT.rglob("*.md")):
        if page.name == "README.md" or page in FUNCTION_FAMILY_LINK_EXCLUSIONS:
            continue
        total += 1
        if page.resolve() not in summary_targets:
            errors.append(f"  missing from SUMMARY.md: {page.relative_to(REPO_ROOT)}")

    return errors, total


def find_summary_orphans(md_files: set[Path]) -> list[str]:
    """Find .md files on disk that are NOT listed in SUMMARY.md."""
    if not SUMMARY_PATH.exists():
        return []

    # Collect all paths referenced from SUMMARY.md
    summary_paths: set[Path] = set()
    for raw_link, _ in extract_links(SUMMARY_PATH):
        path_part = raw_link.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (REPO_ROOT / path_part).resolve()
        summary_paths.add(resolved)

    orphans = []
    for filepath in sorted(md_files):
        resolved = filepath.resolve()
        if resolved in summary_paths:
            continue
        if resolved in SUMMARY_ORPHAN_EXCLUSIONS:
            continue
        # Skip .gitbook includes
        try:
            rel = filepath.relative_to(REPO_ROOT)
        except ValueError:
            continue
        if str(rel).startswith(".gitbook"):
            continue
        orphans.append(f"  {rel}")
    return orphans


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Pinot docs links")
    parser.add_argument("--strict", action="store_true",
                        help="Fail on anchor warnings too")
    parser.add_argument("--warn-only", action="store_true",
                        help="Report issues but always exit 0")
    parser.add_argument("--summary-only", action="store_true",
                        help="Print counts only, no per-file details")
    parser.add_argument("--changed-only", metavar="FILE",
                        help="Only check files listed in FILE (one per line)")
    args = parser.parse_args()

    print("=" * 64)
    print("  Pinot Docs Validation")
    print("=" * 64)
    print(f"  Repo root: {REPO_ROOT}\n")

    all_repo_md_files = all_md_files(REPO_ROOT)
    md_files = all_repo_md_files

    # Optionally filter to only changed files
    changed_md_files = None

    if args.changed_only:
        try:
            changed = set()
            for line in Path(args.changed_only).read_text().strip().splitlines():
                p = (REPO_ROOT / line.strip()).resolve()
                if p.exists() and p.suffix == ".md":
                    changed.add(p)
            md_files = changed
            changed_md_files = changed
            print(f"  Checking {len(md_files)} changed file(s)\n")
        except Exception as e:
            print(f"  Warning: could not read {args.changed_only}: {e}")
            print(f"  Falling back to all {len(md_files)} files\n")
    else:
        print(f"  Checking all {len(md_files)} markdown files\n")

    has_error = False

    # ── CHECK 1: SUMMARY.md ──────────────────────────────────────────
    print("-" * 64)
    print("CHECK 1: SUMMARY.md targets")
    print("-" * 64)
    summary_errors, summary_count = check_summary_targets()
    if summary_errors:
        has_error = True
        print(f"FAIL — {len(summary_errors)} broken / {summary_count} total")
        if not args.summary_only:
            print("\n".join(summary_errors))
    else:
        print(f"PASS — all {summary_count} targets exist")
    print()

    # ── CHECK 2: Broken file links ───────────────────────────────────
    print("-" * 64)
    print("CHECK 2: Broken file links")
    print("-" * 64)
    file_errors, anchor_warnings, total_links = check_broken_links(md_files)
    if file_errors:
        has_error = True
        print(f"FAIL — {len(file_errors)} broken file link(s) / {total_links} checked")
        if not args.summary_only:
            print("\n".join(file_errors))
    else:
        print(f"PASS — all {total_links} file links resolve")
    print()

    # ── CHECK 3: Broken anchors (warning) ────────────────────────────
    print("-" * 64)
    print("CHECK 3: Broken anchors")
    print("-" * 64)
    if anchor_warnings:
        if args.strict:
            has_error = True
            label = "FAIL"
        else:
            label = "WARNING"
        print(f"{label} — {len(anchor_warnings)} broken anchor(s)")
        if not args.summary_only:
            print("\n".join(anchor_warnings))
    else:
        print("PASS — all anchors resolve")
    print()

    # ── CHECK 4: Reachability ────────────────────────────────────────
    print("-" * 64)
    print("CHECK 4: Reachability")
    print("-" * 64)
    orphan_paths = find_orphan_pages(all_repo_md_files)
    if changed_md_files is not None:
        orphan_paths = [p for p in orphan_paths if p in changed_md_files]
    orphans = [f"  {p.relative_to(REPO_ROOT)}" for p in orphan_paths]
    if orphans:
        has_error = True
        print(f"FAIL — {len(orphans)} unlinked page(s)")
        if not args.summary_only:
            print("\n".join(orphans))
    else:
        print("PASS — every markdown page is linked from the docs")
    print()

    # ── CHECK 5: Function family README coverage ────────────────────
    print("-" * 64)
    print("CHECK 5: Function family README coverage")
    print("-" * 64)
    function_link_errors, function_page_count = check_function_family_links(
        changed_md_files
    )
    if function_link_errors:
        has_error = True
        print(
            f"FAIL — {len(function_link_errors)} missing family link(s) / "
            f"{function_page_count} function page(s) checked"
        )
        if not args.summary_only:
            print("\n".join(function_link_errors))
    else:
        print(
            f"PASS — all {function_page_count} function page(s) are linked "
            "from their family README"
        )
    print()

    # ── CHECK 6: Function SUMMARY coverage ───────────────────────────
    print("-" * 64)
    print("CHECK 6: Function SUMMARY coverage")
    print("-" * 64)
    function_summary_errors, function_summary_count = check_function_summary_coverage()
    if function_summary_errors:
        has_error = True
        print(
            f"FAIL — {len(function_summary_errors)} missing SUMMARY link(s) / "
            f"{function_summary_count} function page(s) checked"
        )
        if not args.summary_only:
            print("\n".join(function_summary_errors))
    else:
        print(
            f"PASS — all {function_summary_count} function page(s) are listed "
            "in SUMMARY.md"
        )
    print()

    # ── CHECK 7: Redirect targets ────────────────────────────────────
    print("-" * 64)
    print("CHECK 7: Redirect targets (.gitbook.yaml)")
    print("-" * 64)
    redirect_errors, redirect_count = check_redirects()
    if redirect_errors:
        has_error = True
        print(f"FAIL — {len(redirect_errors)} broken / {redirect_count} total")
        if not args.summary_only:
            print("\n".join(redirect_errors))
    else:
        print(f"PASS — all {redirect_count} redirect targets exist")
    print()

    # ── CHECK 8: Orphan file check ──────────────────────────────────
    print("-" * 64)
    print("CHECK 8: Orphan files (not in SUMMARY.md)")
    print("-" * 64)
    summary_orphans = find_summary_orphans(all_repo_md_files)
    if changed_md_files is not None:
        # In --changed-only mode, only flag orphans that are new/changed files
        changed_rel = {
            f"  {p.relative_to(REPO_ROOT)}" for p in changed_md_files
        }
        summary_orphans = [o for o in summary_orphans if o in changed_rel]
    if summary_orphans:
        has_error = True
        print(f"FAIL — {len(summary_orphans)} file(s) not listed in SUMMARY.md")
        if not args.summary_only:
            print("\n".join(summary_orphans))
    else:
        print("PASS — every .md file is listed in SUMMARY.md")
    print()

    # ── Summary ──────────────────────────────────────────────────────
    print("=" * 64)
    print(f"  Files checked:        {len(md_files)}")
    print(f"  Links checked:        {total_links}")
    print(f"  Broken file links:    {len(file_errors)}")
    print(f"  Broken anchors:       {len(anchor_warnings)}")
    print(f"  Orphan pages:         {len(orphans)}")
    print(f"  Broken SUMMARY refs:  {len(summary_errors)}")
    print(f"  Missing family links: {len(function_link_errors)}")
    print(f"  Missing SUMMARY funcs:{len(function_summary_errors)}")
    print(f"  Broken redirects:     {len(redirect_errors)}")
    print(f"  SUMMARY orphans:      {len(summary_orphans)}")
    print("=" * 64)

    if args.warn_only:
        print("  MODE: --warn-only (exit 0 regardless)")
        return 0

    if has_error:
        print("  RESULT: FAIL")
        return 1
    else:
        print("  RESULT: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
