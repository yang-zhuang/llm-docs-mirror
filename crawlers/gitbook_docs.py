# -*- coding: utf-8 -*-
"""
平台适配器：GitBook 文档站（unsloth）。

官网机制：
1. 页面清单 = 官方 llms.txt，每行 "- [标题](url.md): 简介"。
2. 页面正文 = llms.txt 里的 .md 链接本身（markdown 原文）。
   目录结构 = 官网 URL 路径层级，不加编号。

输出：
  docs/unsloth/...              纯官网 URL 镜像
  state/unsloth.manifest.json   URL 主键的增量状态
  state/unsloth.INDEX.md        按一级路径分组的索引（链接相对 state/）

用法：python crawlers/gitbook_docs.py [--force] [--workers 8]
"""

import argparse
import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"

BASE_URL = "https://unsloth.ai/docs"
LLMS_TXT_URL = BASE_URL + "/llms.txt"
URL_PREFIX = BASE_URL + "/"
LINK_RE = re.compile(r"^- \[(.*?)\]\((https://unsloth\.ai/docs/[^)]+\.md)\)(?::\s*(.*))?$")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) llm-docs-mirror/1.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def fetch(url: str, retries: int = 3) -> str | None:
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                r.encoding = "utf-8"
                return r.text
            print(f"    HTTP {r.status_code} (第 {attempt} 次尝试)")
        except requests.RequestException as e:
            print(f"    请求异常: {e} (第 {attempt} 次尝试)")
        if attempt < retries:
            time.sleep(2 * attempt)
    return None


def fetch_page_list() -> list[dict]:
    text = fetch(LLMS_TXT_URL)
    if text is None:
        sys.exit("FATAL: 无法获取 llms.txt")
    pages = []
    seen = set()
    for line in text.splitlines():
        m = LINK_RE.match(line.strip())
        if not m:
            continue
        title, url, desc = m.group(1), m.group(2), (m.group(3) or "")
        path = url[len(URL_PREFIX):]
        if path in seen:
            continue
        seen.add(path)
        pages.append({"title": title, "url": url, "path": path, "description": desc})
    if not pages:
        sys.exit("FATAL: llms.txt 里没有解析到页面链接，GitBook 格式可能已变化")
    return pages


def main():
    parser = argparse.ArgumentParser(description="GitBook 文档站适配器（unsloth）")
    parser.add_argument("--force", action="store_true", help="强制重写所有文件")
    parser.add_argument("--workers", type=int, default=8, help="并发线程数，默认 8")
    args = parser.parse_args()

    docs_dir = ROOT / "docs" / "unsloth"
    manifest_path = STATE_DIR / "unsloth.manifest.json"
    index_path = STATE_DIR / "unsloth.INDEX.md"

    print(f"来源: unsloth docs | 站点: {BASE_URL} | 线程: {args.workers}")

    pages = fetch_page_list()
    print(f"llms.txt 共 {len(pages)} 页\n")

    old = {}
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})

    def download(page):
        content = fetch(page["url"])
        if content is None or not content.strip():
            return page, None, "下载失败"
        head = content.lstrip()[:200].lower()
        if head.startswith("<!doctype") or head.startswith("<html"):
            return page, None, "返回的是 HTML 而不是 markdown"
        return page, content, ""

    new_files = {}
    n_new = n_updated = n_unchanged = n_failed = 0
    failures = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, (page, content, err) in enumerate(pool.map(download, pages), 1):
            print(f"[{i}/{len(pages)}] {page['title']}")
            if err:
                print(f"    FAILED: {err}")
                failures.append(page)
                n_failed += 1
                continue

            out_path = docs_dir / page["path"]
            rel = out_path.relative_to(ROOT).as_posix()
            sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
            group = page["path"].split("/")[0] if "/" in page["path"] else "(根目录)"
            new_files[page["url"]] = {
                "path": rel,
                "title": page["title"],
                "group": group,
                "description": page["description"],
                "sha256": sha,
                "size": len(content.encode("utf-8")),
            }

            old_sha = old.get(page["url"], {}).get("sha256")
            if old_sha == sha and not args.force:
                n_unchanged += 1
                print("    unchanged")
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(content, encoding="utf-8", newline="\n")
                if old_sha is None:
                    n_new += 1
                    print(f"    NEW -> {rel}")
                else:
                    n_updated += 1
                    print(f"    UPDATED -> {rel}")

    removed = sorted(set(old) - set(new_files))

    lines = ["# unsloth 文档索引", "",
             f"共 {len(new_files)} 页，同步时间: {datetime.now().isoformat(timespec='seconds')}"]
    cur_group = None
    for info in new_files.values():
        if info["group"] != cur_group:
            cur_group = info["group"]
            lines.append(f"\n## {cur_group}\n")
        link = "../" + info["path"].replace(" ", "%20")
        lines.append(f"- [{info['title']}]({link})")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    manifest_path.write_text(json.dumps({
        "source": "unsloth.docs",
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "base_url": BASE_URL,
        "pages_total": len(new_files),
        "files": new_files,
    }, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("\n" + "=" * 50)
    print(f"完成: {n_new} 新增, {n_updated} 更新, {n_unchanged} 未变, {n_failed} 失败")
    if removed:
        print("官网已删除（本地保留，未删除）:")
        for u in removed:
            print(f"  - {u}")
    if failures:
        print("失败页面:")
        for p in failures:
            print(f"  - {p['title']} ({p['url']})")
        sys.exit(1)


if __name__ == "__main__":
    main()
