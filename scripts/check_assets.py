#!/usr/bin/env python3
"""
check_assets.py: fail if index.html references a local file that is missing
on disk or ignored by git (so it would never reach the live site).

Checks every local path in src="", href="", srcset="", CSS url(), and each
entry in the <script id="logo-map"> JSON (resolved under assets/logos/).
Skips anchors, external URLs, data: URIs, and JS template strings (${...}).

Called by build.py after it writes index.html. Also runnable on its own:
    python scripts/check_assets.py              # check the repo
    python scripts/check_assets.py --self-test  # prove the check catches problems
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
LOGO_DIR = "assets/logos"

ATTR = re.compile(r'\b(?:src|href)\s*=\s*"([^"]*)"')
SRCSET = re.compile(r'\bsrcset\s*=\s*"([^"]*)"')
CSS_URL = re.compile(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)')
LOGO_MAP = re.compile(r'<script id="logo-map" type="application/json">(.*?)</script>', re.S)


def local_path(ref: str) -> str | None:
    """Return the repo-relative path for a local reference, or None to skip it."""
    ref = ref.strip()
    if not ref or ref.startswith(("#", "data:", "mailto:", "tel:", "javascript:", "//")) or "${" in ref:
        return None
    parts = urlsplit(ref)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    return path.lstrip("/") or None


def referenced_paths(html: str) -> set[str]:
    refs = set(ATTR.findall(html)) | set(CSS_URL.findall(html))
    for srcset in SRCSET.findall(html):
        refs |= {item.split()[0] for item in srcset.split(",") if item.strip()}
    m = LOGO_MAP.search(html)
    if m:
        refs |= {f"{LOGO_DIR}/{name}" for name in json.loads(m.group(1)).values()}
    return {p for p in map(local_path, refs) if p}


def git_ignored(root: Path, paths: list[str]) -> set[str] | None:
    """Paths git would ignore, or None if git is unavailable here."""
    try:
        res = subprocess.run(["git", "-C", str(root), "check-ignore", "--stdin"],
                             input="\n".join(paths), capture_output=True, text=True)
    except FileNotFoundError:
        return None
    if res.returncode not in (0, 1):  # 0 = some ignored, 1 = none ignored
        return None
    return set(res.stdout.split())


def check(root: Path = ROOT, index: str = "index.html") -> list[str]:
    html = (root / index).read_text(encoding="utf-8")
    paths = sorted(referenced_paths(html))
    problems = [f"missing on disk: {p}" for p in paths if not (root / p).is_file()]
    ignored = git_ignored(root, paths)
    if ignored is None:
        print("check_assets: git unavailable, skipped the git-ignore check", file=sys.stderr)
    else:
        problems += [f"ignored by git (would not be committed): {p}" for p in paths if p in ignored]
    return problems


def self_test() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / ".gitignore").write_text("*.png\n!assets/logos/*.png\n")
        (root / "assets/logos").mkdir(parents=True)
        for f in ("ok.webp", "shot.png", "logos/a.png"):
            (root / "assets" / f).write_bytes(b"x")
        (root / "index.html").write_text(
            '<img src="assets/ok.webp" srcset="assets/ok.webp 1x, assets/gone.webp 2x">'
            '<link href="assets/shot.png"><a href="#top"></a><a href="https://example.com/x.png"></a>'
            '<img src="assets/logos/${f}"><style>@font-face{src:url(assets/fonts/none.woff2)}</style>'
            '<script id="logo-map" type="application/json">{"a":"a.png","b":"b.png"}</script>')
        got = sorted(check(root))
        want = sorted(["missing on disk: assets/gone.webp", "missing on disk: assets/fonts/none.woff2",
                       "missing on disk: assets/logos/b.png",
                       "ignored by git (would not be committed): assets/shot.png"])
        assert got == want, f"self-test failed:\n got  {got}\n want {want}"
    print("check_assets self-test passed")


def main() -> None:
    if "--self-test" in sys.argv:
        self_test()
        return
    problems = check()
    if problems:
        sys.exit("Asset check failed:\n  " + "\n  ".join(problems))
    print("Asset check passed: every local file index.html references exists and is not ignored by git.")


if __name__ == "__main__":
    main()
