#!/usr/bin/env python3
"""Generate the profile stats and language cards from the GitHub GraphQL API.

usage: stats.py <login> <output dir>   (reads GITHUB_TOKEN)
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path

IGNORED = {"HTML", "CSS", "SCSS", "Less", "TeX", "Makefile", "Dockerfile", "CMake", "Jupyter Notebook"}
THEMES = {
    "light": {"bg": "#FFFFFF", "line": "#DFE8F1", "text": "#1D2B3A", "dim": "#5A6B7E", "num": "#136CB3"},
    "dark": {"bg": "#161B22", "line": "#30363D", "text": "#E6EDF3", "dim": "#8B949E", "num": "#7CC0F2"},
}
FONT = "-apple-system,'Segoe UI','PingFang SC',Helvetica,Arial,sans-serif"
QUERY = """query($login:String!){user(login:$login){
  followers{totalCount}
  contributionsCollection{totalCommitContributions contributionCalendar{totalContributions}}
  repositories(first:100,ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC){
    totalCount
    nodes{languages(first:10,orderBy:{field:SIZE,direction:DESC}){
      edges{size node{name color}}}}}
}}"""


def fetch(login: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def card(theme: dict, title: str, body: str, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 {height}" width="420" height="{height}" role="img" aria-label="{escape(title)}">'
        f'<title>{escape(title)}</title>'
        f'<rect x=".5" y=".5" width="419" height="{height - 1}" rx="12" fill="{theme["bg"]}" stroke="{theme["line"]}"/>'
        f'<text x="24" y="36" font-family="{FONT}" font-size="15" font-weight="600" fill="{theme["text"]}">{escape(title)}</text>'
        f"{body}</svg>\n"
    )


def stats_card(theme: dict, items: list[tuple[str, int]]) -> str:
    body = ""
    for i, (label, value) in enumerate(items):
        x, y = 24 + (i % 2) * 196, 84 + (i // 2) * 62
        body += (
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="26" font-weight="600" fill="{theme["num"]}">{value:,}</text>'
            f'<text x="{x}" y="{y + 21}" font-family="{FONT}" font-size="12.5" fill="{theme["dim"]}">{escape(label)}</text>'
        )
    return card(theme, "GitHub activity", body, 180)


def language_card(theme: dict, languages: list[tuple[str, int, str]]) -> str:
    total = sum(size for _, size, _ in languages) or 1
    bar, x = "", 24.0
    for _, size, color in languages:
        width = 372 * size / total
        bar += f'<rect x="{x:.1f}" y="52" width="{width:.1f}" height="10" fill="{color}"/>'
        x += width
    body = f'<clipPath id="r"><rect x="24" y="52" width="372" height="10" rx="5"/></clipPath><g clip-path="url(#r)">{bar}</g>'
    for i, (name, size, color) in enumerate(languages):
        lx, ly = 24 + (i % 2) * 196, 92 + (i // 2) * 28
        body += (
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
            f'<text x="{lx + 18}" y="{ly}" font-family="{FONT}" font-size="13" fill="{theme["text"]}">{escape(name)}'
            f'<tspan fill="{theme["dim"]}"> {100 * size / total:.1f}%</tspan></text>'
        )
    return card(theme, "Languages in public repos", body, 180)


def main() -> None:
    login, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    user = fetch(login)
    repos = user["repositories"]
    sizes, colors = Counter(), {}
    for repo in repos["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name not in IGNORED:
                sizes[name] += edge["size"]
                colors[name] = edge["node"]["color"] or "#8B949E"
    top = [(name, size, colors[name]) for name, size in sizes.most_common(6)]
    activity = user["contributionsCollection"]
    items = [
        ("Contributions, past year", activity["contributionCalendar"]["totalContributions"]),
        ("Commits, past year", activity["totalCommitContributions"]),
        ("Public repos", repos["totalCount"]),
        ("Followers", user["followers"]["totalCount"]),
    ]
    for name, theme in THEMES.items():
        (out / f"stats-{name}.svg").write_text(stats_card(theme, items), encoding="utf-8")
        (out / f"languages-{name}.svg").write_text(language_card(theme, top), encoding="utf-8")
    print(items, [t[0] for t in top])


if __name__ == "__main__":
    main()
