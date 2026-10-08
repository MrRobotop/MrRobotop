#!/usr/bin/env python3
"""Refresh the live stats on this GitHub profile README.

Pulls public numbers from the Hugging Face Hub, pypistats.org and the GitHub API,
then rewrites:

  assets/stats-light.svg, assets/stats-dark.svg, assets/stats-auto.svg   the stats card
  assets/data/stats.json        the numbers behind the card
  assets/data/pypi-daily.json   daily PyPI downloads, kept so totals survive the 180-day API window
  assets/data/badge-*.json      shields.io endpoint badges used in the README
  README.md                     the block between the STATS:START and STATS:END markers

If a source is down, the last known numbers for that source are kept, so the card never breaks.
Standard library only. Runs on GitHub Actions (ubuntu-latest, Python 3.8+).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = ASSETS / "data"

CONFIG = {
    "github_user": "MrRobotop",
    "hf_user": "rishhh",
    "pypi_packages": ["toploss", "clap-family"],
    "preprints": 4,
    "preprints_note": "2026, on Zenodo",
    # Hugging Face repo-name prefix -> project label, in fixed colour order.
    "projects": [("VeriSci", "verisci"), ("SchemaSage", "schemasage")],
}
UA = "MrRobotop-profile-stats/1.0 (+https://github.com/MrRobotop)"

# ---------------------------------------------------------------------------
# Design tokens (shared by every card). Series colours are a validated
# categorical palette; text always uses the ink tokens, never series colours.
# ---------------------------------------------------------------------------
FONT = 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace'
THEMES = {
    "light": {
        "surface": "#f6f8fa", "panel": "#ffffff", "border": "#d0d7de",
        "ink": "#1f2328", "ink2": "#59636e", "muted": "#6e7781", "grid": "#d8dee4",
        "track": "#cde2fb", "s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a",
        "other": "#8c959f", "goodtext": "#006300", "good": "#0ca30c",
        "accent": "#2a78d6", "accent2": "#4a3aa7", "dots": "#59636e",
    },
    "dark": {
        "surface": "#161b22", "panel": "#0d1117", "border": "#30363d",
        "ink": "#f0f6fc", "ink2": "#9198a1", "muted": "#848d97", "grid": "#30363d",
        "track": "#104281", "s1": "#3987e5", "s2": "#d95926", "s3": "#199e70",
        "other": "#6e7681", "goodtext": "#0ca30c", "good": "#0ca30c",
        "accent": "#3987e5", "accent2": "#9085e9", "dots": "#9198a1",
    },
}

BASE_CSS = (
    ".card{fill:var(--surface);stroke:var(--border)}"
    ".panel{fill:var(--panel);stroke:var(--border)}"
    ".rule{stroke:var(--grid);stroke-width:1}"
    ".ink{fill:var(--ink)}.ink2{fill:var(--ink2)}.muted{fill:var(--muted)}"
    ".good{fill:var(--goodtext)}.goodmark{fill:var(--good)}"
    ".h{font-size:16px;font-weight:600;fill:var(--ink)}"
    ".small{font-size:13px;fill:var(--muted)}"
    ".s1{fill:var(--s1)}.s2{fill:var(--s2)}.s3{fill:var(--s3)}.other{fill:var(--other)}"
    ".track{fill:var(--track)}.fill{fill:var(--s1)}"
)


def _vars(theme: dict) -> str:
    return ";".join(f"--{k}:{v}" for k, v in theme.items())


def style_block(mode: str, extra_css: str = "") -> str:
    """CSS for one of three variants: light, dark, or auto (follows the viewer's OS)."""
    theme = THEMES["dark" if mode == "dark" else "light"]
    css = f"svg{{{_vars(theme)};font-family:{FONT}}}"
    if mode == "auto":
        css += f"@media (prefers-color-scheme:dark){{svg{{{_vars(THEMES['dark'])}}}}}"
    return f"<style>{css}{BASE_CSS}{extra_css}</style>"


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def fmt_int(n) -> str:
    return f"{int(n):,}"


def fmt_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')} {d.year}"


def bar_path(x: float, y: float, w: float, h: float, r_right: float) -> str:
    """Rectangle, square on the left (baseline) and optionally rounded on the right (data end)."""
    if r_right <= 0:
        return f"M{x:.1f},{y:.1f}h{w:.1f}v{h:.1f}h{-w:.1f}Z"
    r = min(r_right, w / 2, h / 2)
    return (
        f"M{x:.1f},{y:.1f}H{x + w - r:.1f}A{r},{r} 0 0 1 {x + w:.1f},{y + r:.1f}"
        f"V{y + h - r:.1f}A{r},{r} 0 0 1 {x + w - r:.1f},{y + h:.1f}H{x:.1f}Z"
    )


# ---------------------------------------------------------------------------
# Data sources
# ---------------------------------------------------------------------------
def get_json(url: str, headers: dict | None = None, timeout: int = 30, tries: int = 3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "application/json", **(headers or {})}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as err:
            last = err
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def project_of(repo_id: str) -> str:
    name = repo_id.split("/", 1)[-1].lower()
    for label, prefix in CONFIG["projects"]:
        if name.startswith(prefix):
            return label
    return "Other"


def fetch_hf(user: str) -> dict:
    expand = "&expand%5B%5D=downloadsAllTime&expand%5B%5D=downloads"
    base = "https://huggingface.co/api"
    models = get_json(f"{base}/models?author={user}&limit=1000{expand}")
    datasets = get_json(f"{base}/datasets?author={user}&limit=1000{expand}")
    spaces = get_json(f"{base}/spaces?author={user}&limit=1000")
    projects = {label: {"models": 0, "datasets": 0} for label, _ in CONFIG["projects"]}
    projects["Other"] = {"models": 0, "datasets": 0}
    for kind, repos in (("models", models), ("datasets", datasets)):
        for repo in repos:
            projects[project_of(repo["id"])][kind] += int(repo.get("downloadsAllTime") or 0)
    return {
        "models": len(models),
        "datasets": len(datasets),
        "spaces": len(spaces),
        "model_downloads": sum(int(m.get("downloadsAllTime") or 0) for m in models),
        "model_downloads_30d": sum(int(m.get("downloads") or 0) for m in models),
        "dataset_downloads": sum(int(d.get("downloadsAllTime") or 0) for d in datasets),
        "dataset_downloads_30d": sum(int(d.get("downloads") or 0) for d in datasets),
        "projects": projects,
    }


def fetch_pypi(packages: list, daily: dict) -> dict:
    """Merge pypistats daily rows (excluding mirrors) into `daily`, then total them."""
    for pkg in packages:
        rows = get_json(f"https://pypistats.org/api/packages/{pkg}/overall?mirrors=false")["data"]
        store = daily.setdefault(pkg, {})
        for row in rows:
            if row.get("category") == "without_mirrors":
                store[row["date"]] = int(row["downloads"])
    by_package = {pkg: sum(daily.get(pkg, {}).values()) for pkg in packages}
    return {"packages": len(packages), "downloads": sum(by_package.values()), "by_package": by_package}


def fetch_github(user: str, token: str | None) -> dict:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    profile = get_json(f"https://api.github.com/users/{user}", headers)
    stars, page = 0, 1
    while True:
        repos = get_json(
            f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}", headers
        )
        stars += sum(int(r.get("stargazers_count") or 0) for r in repos)
        if len(repos) < 100:
            break
        page += 1
    return {"public_repos": int(profile["public_repos"]), "stars": stars}


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def collect(prev: dict) -> dict:
    stats = {"preprints": CONFIG["preprints"]}
    fresh = False
    daily = load_json(DATA / "pypi-daily.json", {})
    sources = {
        "hf": lambda: fetch_hf(CONFIG["hf_user"]),
        "pypi": lambda: fetch_pypi(CONFIG["pypi_packages"], daily),
        "github": lambda: fetch_github(CONFIG["github_user"], os.environ.get("GITHUB_TOKEN")),
    }
    for key, fetch in sources.items():
        try:
            stats[key] = fetch()
            fresh = True
            print(f"[ok] {key}")
        except Exception as err:  # keep the last known numbers for this source
            if key not in prev:
                raise SystemExit(f"[fail] {key} and no previous numbers to fall back on: {err}")
            stats[key] = prev[key]
            print(f"[warn] {key} unavailable, keeping previous numbers: {err}")
    (DATA / "pypi-daily.json").write_text(json.dumps(daily, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    stats["updated"] = today if fresh else prev.get("updated", today)
    return stats


# ---------------------------------------------------------------------------
# Stats card
# ---------------------------------------------------------------------------
def derived(stats: dict) -> dict:
    hf = stats["hf"]
    total = hf["model_downloads"] + hf["dataset_downloads"]
    last30 = hf["model_downloads_30d"] + hf["dataset_downloads_30d"]
    segments = []
    slot = ["s1", "s2"]
    for i, (label, _) in enumerate(CONFIG["projects"]):
        segments.append((f"{label} models", hf["projects"].get(label, {}).get("models", 0), slot[i] if i < 2 else "other"))
    segments.append(("Datasets", hf["dataset_downloads"], "s3"))
    segments.append(("Other models", hf["projects"].get("Other", {}).get("models", 0), "other"))
    segments = [s for s in segments if s[1] > 0]
    return {"total": total, "last30": last30, "segments": segments}


def stacked_bar(segments, x: float, y: float, width: float, height: float) -> str:
    total = sum(v for _, v, _ in segments) or 1
    gap = 2.0
    usable = width - gap * (len(segments) - 1)
    widths = [max(3.0, usable * v / total) for _, v, _ in segments]
    scale = usable / sum(widths)
    widths = [w * scale for w in widths]
    out, cx = [], x
    for i, ((label, value, slot), w) in enumerate(zip(segments, widths)):
        r = 4 if i == len(segments) - 1 else 0
        out.append(
            f'<path class="{slot}" d="{bar_path(cx, y, w, height, r)}">'
            f"<title>{esc(label)}: {fmt_int(value)}</title></path>"
        )
        cx += w + gap
    return "".join(out)


def legend(segments, x: float, y: float, width: float) -> str:
    """One row per segment: swatch, name, and the value right-aligned like a table column."""
    step = 22 if len(segments) <= 3 else 19
    out = []
    for i, (label, value, slot) in enumerate(segments):
        cy = y + i * step
        out.append(f'<rect class="{slot}" x="{x:.1f}" y="{cy - 10:.1f}" width="10" height="10" rx="2"/>')
        out.append(f'<text class="ink2" x="{x + 18:.1f}" y="{cy:.1f}" font-size="13.5">{esc(label)}</text>')
        out.append(
            f'<text class="ink" x="{x + width:.1f}" y="{cy:.1f}" font-size="13.5" font-weight="600" '
            f'text-anchor="end" style="font-variant-numeric:tabular-nums">{fmt_int(value)}</text>'
        )
    return "".join(out)


def stats_svg(stats: dict, mode: str) -> str:
    W, H = 840, 320
    d = derived(stats)
    hf, gh, pypi = stats["hf"], stats["github"], stats["pypi"]
    plural = lambda n, word: f"{n} {word}{'' if n == 1 else 's'}"
    tiles = [
        (fmt_int(hf["models"]), "models on Hugging Face",
         f"{plural(hf['datasets'], 'dataset')} · {plural(hf['spaces'], 'Space')}"),
        (fmt_int(gh["stars"]), "GitHub stars", f"across {gh['public_repos']} public repos"),
        (fmt_int(pypi["downloads"]), "PyPI downloads", f"{pypi['packages']} libraries, excl. mirrors"),
        (fmt_int(stats["preprints"]), "preprints", CONFIG["preprints_note"]),
    ]
    summary = (
        f"{fmt_int(d['total'])} Hugging Face downloads, {fmt_int(d['last30'])} in the last 30 days. "
        f"{hf['models']} models. {gh['stars']} GitHub stars. {fmt_int(pypi['downloads'])} PyPI downloads. "
        f"{stats['preprints']} preprints. Updated {fmt_date(stats['updated'])}."
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">',
        f'<title id="t">{esc(summary)}</title>',
        style_block(mode),
        f'<rect class="card" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14"/>',
        '<text class="h" x="28" y="42">Live stats</text>',
        f'<text class="small" x="{W - 28}" y="42" text-anchor="end">Updated {esc(fmt_date(stats["updated"]))} · refreshes daily</text>',
        # Hero figure
        f'<text class="ink" x="26" y="112" font-size="48" font-weight="600">{fmt_int(d["total"])}</text>',
        '<text class="ink2" x="28" y="140" font-size="14.5">Hugging Face downloads, all time</text>',
        '<path class="goodmark" d="M28,167 l6,-10 l6,10 z"/>',
        f'<text x="46" y="167" font-size="14"><tspan class="good" font-weight="600">+{fmt_int(d["last30"])}</tspan>'
        '<tspan class="ink2"> in the last 30 days</tspan></text>',
        # Breakdown
        '<text class="small" x="360" y="80">Downloads by project</text>',
        stacked_bar(d["segments"], 360, 92, 452, 16),
        legend(d["segments"], 360, 140, 452),
        f'<line class="rule" x1="28" y1="214" x2="{W - 28}" y2="214"/>',
    ]
    for i, (value, label, sub) in enumerate(tiles):
        x = 28 + i * 196
        parts.append(f'<text class="ink" x="{x - 1}" y="258" font-size="28" font-weight="600">{esc(value)}</text>')
        parts.append(f'<text class="ink2" x="{x}" y="281" font-size="14">{esc(label)}</text>')
        parts.append(f'<text class="muted" x="{x}" y="301" font-size="12.5">{esc(sub)}</text>')
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# README block and endpoint badges
# ---------------------------------------------------------------------------
def readme_block(stats: dict) -> str:
    d = derived(stats)
    hf, gh, pypi = stats["hf"], stats["github"], stats["pypi"]
    alt = (
        f"Live stats: {fmt_int(d['total'])} Hugging Face downloads ({fmt_int(d['last30'])} in the last 30 days), "
        f"{hf['models']} models, {gh['stars']} GitHub stars across {gh['public_repos']} public repos, "
        f"{fmt_int(pypi['downloads'])} PyPI downloads, {stats['preprints']} preprints. Updated {fmt_date(stats['updated'])}."
    )
    breakdown = " · ".join(f"{label} {fmt_int(value)}" for label, value, _ in d["segments"])
    by_pkg = " · ".join(
        f"{pkg} {fmt_int(pypi['by_package'][pkg])}" for pkg in CONFIG["pypi_packages"] if pkg in pypi["by_package"]
    )
    rows = [
        ("Hugging Face downloads, all time", f"{fmt_int(d['total'])} ({breakdown})"),
        ("Hugging Face downloads, last 30 days", fmt_int(d["last30"])),
        ("Models, datasets, Spaces", f"{hf['models']}, {hf['datasets']}, {hf['spaces']}"),
        ("GitHub stars", f"{fmt_int(gh['stars'])} across {gh['public_repos']} public repos"),
        ("PyPI downloads, excluding mirrors", f"{fmt_int(pypi['downloads'])} ({by_pkg})"),
        ("Preprints", f"{stats['preprints']} ({CONFIG['preprints_note']})"),
    ]
    table = "\n".join(f"| {a} | {b} |" for a, b in rows)
    return (
        "<picture>\n"
        f'  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">\n'
        f'  <img alt="{esc(alt)}" src="assets/stats-light.svg" width="100%">\n'
        "</picture>\n\n"
        "<details>\n<summary>Stats as a table</summary>\n\n"
        "| Metric | Value |\n| :-- | :-- |\n"
        f"{table}\n\n"
        f"Updated {fmt_date(stats['updated'])}; refreshed daily by GitHub Actions.\n\n"
        "</details>"
    )


def update_readme(stats: dict) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        print("[warn] README.md not found; skipped")
        return
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- STATS:START -->", "<!-- STATS:END -->"
    if start not in text or end not in text:
        print("[warn] STATS markers missing; README left unchanged")
        return
    block = readme_block(stats)
    new = re.sub(
        re.escape(start) + r".*?" + re.escape(end),
        lambda _m: f"{start}\n{block}\n{end}",
        text,
        count=1,
        flags=re.S,
    )
    if new != text:
        path.write_text(new, encoding="utf-8")


def write_badges(stats: dict) -> None:
    d = derived(stats)
    projects = stats["hf"]["projects"]
    badges = {
        "hf-downloads": ("HF downloads", fmt_int(d["total"]), "FFD21E", "huggingface"),
        "verisci": ("model downloads", fmt_int(projects.get("VeriSci", {}).get("models", 0)), "2a78d6", "huggingface"),
        "schemasage": ("model downloads", fmt_int(projects.get("SchemaSage", {}).get("models", 0)), "2a78d6", "huggingface"),
        "schemasage-data": ("dataset downloads", fmt_int(projects.get("SchemaSage", {}).get("datasets", 0)), "2a78d6", "huggingface"),
        "pypi-downloads": ("PyPI downloads", fmt_int(stats["pypi"]["downloads"]), "2a78d6", "pypi"),
    }
    for name, (label, message, color, logo) in badges.items():
        body = {"schemaVersion": 1, "label": label, "message": message, "color": color,
                "namedLogo": logo, "style": "flat-square", "cacheSeconds": 3600}
        (DATA / f"badge-{name}.json").write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    prev = load_json(DATA / "stats.json", {})
    stats = collect(prev)
    (DATA / "stats.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for mode in ("light", "dark", "auto"):
        (ASSETS / f"stats-{mode}.svg").write_text(stats_svg(stats, mode) + "\n", encoding="utf-8")
    write_badges(stats)
    update_readme(stats)
    print(json.dumps(stats, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
