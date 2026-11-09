# -*- coding: utf-8 -*-
"""
平台适配器：HuggingFace 文档站（trl / transformers）。

官网机制：
1. 页面清单 = index 页 HTML 里内嵌的 SideMenu JSON（chapters → sections，可嵌套）。
   章节目录名按官网 chapters 顺序自动生成两位序号 + 章节标题 slug，
   所以目录顺序 = 官网侧边栏顺序，官网改组会自动跟随。
2. 页面正文 = 每个页面 URL 加 .md 后缀的 markdown 原文，零转换损失。

输出（统一仓库 llm-docs-mirror）：
  docs/<lib>/<章节>/...     纯官网文档镜像
  state/<lib>.manifest.json  URL 主键的增量状态
  state/<lib>.SUMMARY.md     按章节分组的阅读索引（链接相对 state/）

用法：
  python crawlers/hf_docs.py trl
  python crawlers/hf_docs.py transformers
  python crawlers/hf_docs.py trl --force
  python crawlers/hf_docs.py transformers --workers 3
"""

import argparse
import hashlib
import html as html_lib
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) llm-docs-mirror/1.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def slugify(title: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]+", "_", title.lower()).strip("_") or "unknown"


def fetch(url: str, retries: int = 5) -> str | None:
    """GET 一个 URL。429/503 按 Retry-After 退避（官方 CloudFront 按 IP 限流）。"""
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                r.encoding = "utf-8"
                return r.text
            if r.status_code in (429, 503):
                wait = int(r.headers.get("Retry-After") or 30)
                wait = min(max(wait, 5), 300) + random.uniform(0, 5)
                print(f"    限流 HTTP {r.status_code}，等待 {int(wait)}s 后重试 (第 {attempt} 次)")
                if attempt < retries:
                    time.sleep(wait)
                    continue
            print(f"    HTTP {r.status_code} (第 {attempt} 次尝试)")
        except requests.RequestException as e:
            print(f"    请求异常: {e} (第 {attempt} 次尝试)")
        if attempt < retries:
            time.sleep(3 * attempt)
    return None


def flatten_sections(sections, chapter, chapter_dir, groups, pages):
    for sec in sections:
        if "url" in sec:
            pages.append({
                "chapter": chapter,
                "chapter_dir": chapter_dir,
                "groups": groups,
                "title": sec["title"],
                "url_path": sec["url"],
            })
        else:
            flatten_sections(sec["sections"], chapter, chapter_dir,
                             groups + [sec["title"]], pages)


def fetch_sidebar_pages(base_url: str, lib: str) -> list[dict]:
    html_text = fetch(f"{base_url}/docs/{lib}/index")
    if html_text is None:
        sys.exit(f"FATAL: 无法获取 {lib} 文档首页，检查网络或换 --base-url")

    m = re.search(r'data-target="SideMenu" data-props="([^"]*)"', html_text)
    if m is None:
        sys.exit("FATAL: 页面里找不到 SideMenu JSON，官网结构可能已变化")

    props = json.loads(html_lib.unescape(m.group(1)))
    pages = []
    for idx, chapter in enumerate(props["chapters"]):
        # 序号按官网 chapters 顺序自动生成，不写死；slug 与官网章节标题一一对应
        chapter_dir = f"{idx:02d}_{slugify(chapter['title'])}"
        flatten_sections(chapter["sections"], chapter["title"], chapter_dir, [], pages)
    return pages


def main():
    parser = argparse.ArgumentParser(description="HuggingFace 文档站适配器")
    parser.add_argument("library", help="文档库：trl / transformers")
    parser.add_argument("--base-url", default="https://hf-mirror.com",
                        help="默认 https://hf-mirror.com；代理稳定时可换 https://huggingface.co")
    parser.add_argument("--force", action="store_true", help="强制重写所有文件")
    parser.add_argument("--workers", type=int, default=3,
                        help="并发线程数，默认 3（官方 CDN 限流，不建议超过 4）")
    args = parser.parse_args()

    lib = args.library
    base_url = args.base_url.rstrip("/")
    docs_dir = ROOT / "docs" / lib
    manifest_path = STATE_DIR / f"{lib}.manifest.json"
    summary_path = STATE_DIR / f"{lib}.SUMMARY.md"

    print(f"来源: {lib} docs | 站点: {base_url} | 线程: {args.workers}")
    print(f"输出: {docs_dir}")

    pages = fetch_sidebar_pages(base_url, lib)
    print(f"官网侧边栏共 {len(pages)} 页；章节顺序: " +
          ", ".join(sorted({p["chapter_dir"] for p in pages})) + "\n")

    old = {}
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})

    def download(page):
        content = fetch(base_url + page["url_path"] + ".md")
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
            label = " / ".join([page["chapter"]] + page["groups"] + [page["title"]])
            print(f"[{i}/{len(pages)}] {label}")
            if err:
                print(f"    FAILED: {err}")
                failures.append(page)
                n_failed += 1
                continue

            out_path = docs_dir / page["chapter_dir"]
            for g in page["groups"]:
                out_path = out_path / slugify(g)
            out_path = out_path / f"{page['url_path'].rsplit('/', 1)[-1]}.md"
            rel = out_path.relative_to(ROOT).as_posix()
            official_url = "https://huggingface.co" + page["url_path"]

            if official_url in new_files:
                print(f"    SKIP: 目录路径重复（{rel}）")
                continue

            sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
            new_files[official_url] = {
                "path": rel,
                "title": page["title"],
                "chapter": page["chapter"],
                "groups": page["groups"],
                "sha256": sha,
                "size": len(content.encode("utf-8")),
            }

            old_sha = old.get(official_url, {}).get("sha256")
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

    # 索引放 state/，链接从 state/ 出发需加 ../
    lines = [f"# {lib} 文档索引", "",
             f"共 {len(new_files)} 页，同步时间: {datetime.now().isoformat(timespec='seconds')}"]
    cur_chapter = None
    cur_groups = None
    for page in pages:
        official_url = "https://huggingface.co" + page["url_path"]
        info = new_files.get(official_url)
        if not info:
            continue
        if page["chapter"] != cur_chapter:
            cur_chapter = page["chapter"]
            cur_groups = None
            lines.append(f"\n## {page['chapter_dir']} {cur_chapter}\n")
        if page["groups"] != cur_groups:
            cur_groups = page["groups"]
            if cur_groups:
                lines.append(f"\n### {' / '.join(cur_groups)}\n")
        lines.append(f"- [{page['title']}](../{info['path']})")
    lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    manifest_path.write_text(json.dumps({
        "source": f"{lib}.docs",
        "fetched_at": datetime.now().isoformat(timespec="seconds"),
        "base_url": base_url,
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
            print(f"  - {p['title']} ({base_url}{p['url_path']}.md)")
        sys.exit(1)


if __name__ == "__main__":
    main()
