#!/usr/bin/env python3
"""Обновляет строку GitHub Stats в profile.svg (repos, stars, followers, commits)."""
import json
import os
import re
import urllib.request

USER = "ivan-denysov"
SVG = os.path.join(os.path.dirname(__file__), "profile.svg")


def api(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={
        "Accept": accept,
        "User-Agent": USER,
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
           if os.environ.get("GITHUB_TOKEN") else {}),
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    user = api(f"https://api.github.com/users/{USER}")
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100")
    stars = sum(r["stargazers_count"] for r in repos)
    commits = api(
        f"https://api.github.com/search/commits?q=author:{USER}&per_page=1"
    )["total_count"]

    text = open(SVG, encoding="utf-8").read()
    text = re.sub(
        r"Repos: \d+ \| Stars: \d+ \| Followers: \d+",
        f"Repos: {user['public_repos']} | Stars: {stars} "
        f"| Followers: {user['followers']}",
        text,
    )
    text = re.sub(r"Commits: \d+", f"Commits: {commits}", text)
    open(SVG, "w", encoding="utf-8").write(text)
    print(f"Repos: {user['public_repos']}, Stars: {stars}, "
          f"Followers: {user['followers']}, Commits: {commits}")


if __name__ == "__main__":
    main()
