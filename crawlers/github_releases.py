# -*- coding: utf-8 -*-
"""
平台适配器：GitHub Releases 更新日志（huggingface/trl）。

官网机制：GitHub 官方 API /repos/<owner>/<repo>/releases?per_page=100&page=N
返回 JSON，body 字段就是 release notes 的 markdown 原文，零转换损失。
匿名 60 次/小时（按 IP），403 时按 X-RateLimit-Reset 自动等待；
设置环境变量 GITHUB_TOKEN 可提升到 5000 次/小时。

输出：
  releases/<repo>/...                      按官网 tag 命名的更新日志
  state/releases-<repo>.manifest.json      URL 主键的增量状态
  state/releases-<repo>.INDEX.md           版本索引

用法：python crawlers/github_releases.py huggingface/trl [--force]
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
API_BASE = "https://api.github.com"

HEADERS = {
    "User-Agent": "llm-docs-mirror/1.0",
    "Accept": "application/vnd.github+json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def sanitize_tag(tag: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", tag)


def api_get(url: str, token: str | None, retries: int = 3):
    headers = dict(HEADERS)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 429):
                reset = r.headers.get("X-RateLimit-Reset")
                if reset:
                    wait = min(max(0, int(reset) - int(time.time())) + 5, 3600)
                    print(f"    API 限流，等待 {wait}s 后自动重试（可设 GITHUB_TOKEN 提高限额）")
                    if attempt < retries:
                        time.sleep(wait)
                        continue
                print(f"    HTTP {r.status_code} (第 {attempt} 次尝试)")
            else:
                print(f"    HTTP {r.status_code} (第 {attempt} 次尝试)")
        except requests.RequestException as e:
            print(f"    请求异常: {e} (第 {attempt} 次尝试)")
        if attempt < retries:
            time.sleep(3 * attempt)
    return None


def fetch_all(repo: str, token: str | None):
    all_releases = []
    page = 1
    while True:
        print(f"  拉取第 {page} 页 (per_page=100)...")
        data = api_get(f"{API_BASE}/repos/{repo}/releases?per_page=100&page={page}", token)
        if data is None:
            return None
        all_releases.extend(data)
        if len(data) < 100:
            break
        page += 1
        time.sleep(0.5)
    return all_releases


def main():
    parser = argparse.ArgumentParser(description="GitHub Releases 适配器")
    parser.add_argument("repo", help="仓库，格式 owner/repo，例如 huggingface/trl")
    parser.add_argument("--force", action="store_true", help="强制重写所有文件")
    args = parser.parse_args()

    repo = args.repo
    if not re.fullmatch(r"[\w.\-]+/[\w.\-]+", repo):
        sys.exit(f"FATAL: repo 格式应为 owner/repo，收到: {repo!r}")

    short = repo.split("/")[-1]
    token = os.environ.get("GITHUB_TOKEN")
    releases_dir = ROOT / "releases" / short
    manifest_path = STATE_DIR / f"releases-{short}.manifest.json"
    index_path = STATE_DIR / f"releases-{short}.INDEX.md"

    print(f"来源: {repo} releases | 输出: {releases_dir}")

    releases = fetch_all(repo, token)
    if releases is None:
        sys.exit("FATAL: 拉取 releases 失败")
    print(f"共 {len(releases)} 个 release\n")

    old = {}
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})

    new_files = {}
    n_new = n_updated = n_unchanged = 0

    for rel in releases:
        if rel.get("draft"):
            continue
        tag = rel["tag_name"]
        out_path = releases_dir / (sanitize_tag(tag) + ".md")
        path = out_path.relative_to(ROOT).as_posix()

        body = (rel.get("body") or "").replace("\r\n", "\n")
        header = (f"# {rel.get('name') or tag}\n\n"
                  f"- Tag: `{tag}`\n"
                  f"- 发布时间: {rel.get('published_at') or ''}\n"
                  f"- 链接: {rel['html_url']}\n"
                  f"- Prerelease: {'是' if rel.get('prerelease') else '否'}\n\n"
                  f"---\n\n")
        content = header + (body if body.strip() else "（此 release 没有正文）\n")
        sha = hashlib.sha256(content.encode("utf-8")).hexdigest()

        new_files[rel["html_url"]] = {
            "path": path,
            "tag": tag,
            "name": rel.get("name") or tag,
            "published_at": rel.get("published_at") or "",
            "prerelease": bool(rel.get("prerelease")),
            "sha256": sha,
            "size": len(content.encode("utf-8")),
        }

        old_sha = old.get(rel["html_url"], {}).get("sha256")
        if old_sha == sha and not args.force:
            n_unchanged += 1
            print(f"  unchanged: {tag}")
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8", newline="\n")
            if old_sha is None:
                n_new += 1
                print(f"  NEW -> {path}")
            else:
                n_updated += 1
                print(f"  UPDATED -> {path}")

    removed = sorted(set(old) - set(new_files))

    lines = [f"# {repo} Releases 索引", "",
             f"共 {len(new_files)} 个 release，同步时间: {datetime.now().isoformat(timespec='seconds')}",
             "", "| 版本 | 发布时间 | Prerelease | 文件 |", "|---|---|---|---|"]
    for info in new_files.values():
        flag = " ⚠️" if info["prerelease"] else ""
        lines.append(f"| [{info['name']}](../{info['path']}){flag} | "
                     f"{info['published_at'][:10]} | {'是' if info['prerelease'] else '否'} | "
                     f"[{info['tag']}](../{info['path']}) |")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    manifest_path.write_text(json.dumps({
        "source": f"{short}.releases",
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "base_url": repo,
        "pages_total": len(new_files),
        "files": new_files,
    }, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("\n" + "=" * 50)
    print(f"完成: {n_new} 新增, {n_updated} 更新, {n_unchanged} 未变")
    if removed:
        print("GitHub 上已删除（本地保留，未删除）:")
        for u in removed:
            print(f"  - {u}")


if __name__ == "__main__":
    main()
