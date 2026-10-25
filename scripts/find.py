"""Find Agent Skills on GitHub via multiple sources, optimized for Chinese users.

Usage:
    python find.py "中文 PDF 处理"
    python find.py "React 编码"
    python find.py "我想找一个能帮我写测试的 skill"
    python find.py --min-stars 100 "数据库"

Environment:
    GITHUB_TOKEN (optional) — increase GitHub Search API rate limit
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests


# ---------- sources ----------

GITHUB_API = "https://api.github.com"
AWESOME_CLAUDE_URL = (
    "https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/README.md"
)
SKILLS_SH_API = "https://skills.sh/api/search"  # may 404 if changed


def search_github(query: str, language: str | None, min_stars: int) -> list[dict[str, Any]]:
    """GitHub Search API for repos matching query."""
    parts = [query, "agent-skill"]
    if language == "zh":
        parts += ["language:zh"]
    parts.append(f"stars:>={min_stars}")
    q = "+".join(parts)
    url = f"{GITHUB_API}/search/repositories?q={q}&sort=stars&per_page=15"
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception as e:
        print(f"  [WARN] GitHub search failed: {e}", file=sys.stderr)
        return []
    return [
        {
            "name": item["full_name"],
            "url": item["html_url"],
            "stars": item["stargazers_count"],
            "description": item.get("description") or "",
            "updated": item.get("updated_at", "")[:10],
            "source": "github",
        }
        for item in items
    ]


def search_awesome(query: str) -> list[dict[str, Any]]:
    """Fetch awesome-claude-skills README and filter lines matching query."""
    try:
        r = requests.get(AWESOME_CLAUDE_URL, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"  [WARN] awesome fetch failed: {e}", file=sys.stderr)
        return []

    q_words = set(re.split(r"\W+", query.lower()))
    q_words -= {"", "的", "我", "想", "找", "一个", "能", "帮", "我"}
    if not q_words:
        q_words = {"skill"}

    results = []
    for line in r.text.splitlines():
        if "github.com/" not in line:
            continue
        line_lower = line.lower()
        if not any(w in line_lower for w in q_words):
            continue
        m = re.search(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", line)
        if not m:
            continue
        slug = m.group(1).rstrip("/").rstrip(")")
        results.append(
            {
                "name": slug,
                "url": f"https://github.com/{slug}",
                "stars": 0,
                "description": line.strip()[:200],
                "updated": "",
                "source": "awesome",
            }
        )
    return results


def search_skills_sh(query: str) -> list[dict[str, Any]]:
    """skills.sh search (may not have public API — fail silently)."""
    try:
        r = requests.get(SKILLS_SH_API, params={"q": query}, timeout=10)
        r.raise_for_status()
        data = r.json()
        return [
            {
                "name": item.get("name", ""),
                "url": item.get("url", ""),
                "installs": int(item.get("installs") or 0),
                "stars": 0,
                "description": item.get("description", ""),
                "updated": "",
                "source": "skills.sh",
            }
            for item in data.get("skills", [])
        ]
    except Exception:
        return []


# ---------- aggregator ----------

def aggregate(results_per_source: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Merge by URL, sum cross-source hits, sort by score."""
    merged: dict[str, dict[str, Any]] = {}
    for items in results_per_source:
        for item in items:
            url = item.get("url") or ""
            if not url:
                continue          # 没有 URL 的条目无法去重也无法安装，直接丢弃
            if url not in merged:
                merged[url] = {**item, "cross_source_hits": 0}
            merged[url]["cross_source_hits"] += 1
            if item["stars"] > merged[url]["stars"]:
                merged[url]["stars"] = item["stars"]
    scored = sorted(
        merged.values(),
        key=lambda x: (x["stars"] * 0.6 + x["cross_source_hits"] * 1000 * 0.4),
        reverse=True,
    )
    return scored


# ---------- formatter ----------

EMOJI_RANK = ["🥇", "🥈", "🥉", "4.", "5.", "6.", "7.", "8.", "9.", "10."]


def print_results(query: str, results: list[dict[str, Any]], top: int) -> None:
    print(f"\n{'=' * 60}")
    print(f"  Skill Finder ZH — 搜索:{query}")
    print(f"{'=' * 60}\n")

    if not results:
        print("[!] 没找到结果。试试其他关键词,或降低 --min-stars。\n")
        return

    for i, item in enumerate(results[:top], 1):
        emoji = EMOJI_RANK[i - 1] if i - 1 < len(EMOJI_RANK) else f"{i}."
        stars = item["stars"]
        installs = item.get("installs") or 0
        if installs:
            stars_str = f"({installs:,} installs)"
        else:
            stars_str = f"({stars:,} ⭐)" if stars > 0 else ""
        name = item["name"] or "(unknown)"
        print(f"{emoji} {name} {stars_str}")
        print(f"   URL: {item['url']}")
        desc = item.get("description", "").strip()
        if desc:
            print(f"   简介:{desc[:150]}")
        if item.get("updated"):
            print(f"   更新:{item['updated']}")
        if "github.com/" in item["url"]:
            slug = item["url"].split("github.com/")[-1]
            print(f"   安装:npx skills add {slug}")
        print(f"   数据源:{item['source']} (cross-source hits: {item['cross_source_hits']})")
        print()

    print("💡 下一步:")
    print("   - 直接装:npx skills add <owner/repo>")
    print("   - 官方 CLI 直接搜:npx skills find '<关键词>'")
    print("   - 再找 5 个相关:跑 python find.py '<相关关键词>'")
    print("   - 调权重:--min-stars 50 或更高\n")


# ---------- main ----------

def main() -> int:
    p = argparse.ArgumentParser(description="Find Agent Skills on GitHub (Chinese-optimized)")
    p.add_argument("query", nargs="+", help="search keywords (Chinese or English)")
    p.add_argument("--min-stars", type=int, default=10, help="minimum star count")
    p.add_argument("--language", choices=["zh", "en", "any"], default="any")
    p.add_argument("--top", type=int, default=10, help="number of results to show")
    args = p.parse_args()

    query = " ".join(args.query)
    language = args.language if args.language != "any" else None

    print(f"[*] 搜索中... (min-stars={args.min_stars}, language={args.language or 'any'})")

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {
            ex.submit(search_github, query, language, args.min_stars): "github",
            ex.submit(search_awesome, query): "awesome",
            ex.submit(search_skills_sh, query): "skills.sh",
        }
        results_per_source = []
        for fut in as_completed(futures):
            results_per_source.append(fut.result())

    merged = aggregate(results_per_source)
    print_results(query, merged, args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())