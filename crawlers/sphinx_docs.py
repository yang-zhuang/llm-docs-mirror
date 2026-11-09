# -*- coding: utf-8 -*-
"""
平台适配器：Sphinx / Read the Docs（ms-swift 中文文档）。

官网机制：
1. 页面清单 = searchindex.js 里 docnames / filenames / titles 三个数组按位对应，
   filenames 给出源文件的真实后缀（.md 或 .rst）。
2. 页面正文 = _sources/<源文件名>.txt，Sphinx 拷出的源文件原文，零转换损失。
   目录结构 = 官网 docname 路径层级，不加编号。

输出：
  docs/swift/...              纯官网 docname 镜像
  state/swift.manifest.json   URL 主键的增量状态
  state/swift.INDEX.md        按一级目录分组的中文标题索引

用法：python crawlers/sphinx_docs.py [--force] [--workers 4]
"""

import argparse
import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"

BASE_URL = "https://swift.readthedocs.io/zh-cn/latest"
SEARCHINDEX_URL = BASE_URL + "/searchindex.js"
SOURCES_URL = BASE_URL + "/_sources/"

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
    text = fetch(SEARCHINDEX_URL)
    if text is None:
        sys.exit("FATAL: 无法获取 searchindex.js")
    data = json.loads(text[text.find("{"):text.rfind("}") + 1])
    docnames, filenames, titles = data["docnames"], data["filenames"], data["titles"]
    if not (len(docnames) == len(filenames) == len(titles)):
        sys.exit("FATAL: searchindex.js 三个数组长度不一致，Sphinx 版本可能已变化")
    pages = []
    for docname, filename, title in zip(docnames, filenames, titles):
        ext = filename.rsplit(".", 1)[-1]
        pages.append({
            "docname": docname,
            "filename": filename,
            "title": title,
            "ext": ext,
            "src_url": SOURCES_URL + filename + ".txt",
            "url": BASE_URL + "/" + docname + ".html",
        })
    return pages


def main():
    parser = argparse.ArgumentParser(description="Sphinx/ReadTheDocs 适配器（ms-swift）")
    parser.add_argument("--force", action="store_true", help="强制重写所有文件")
    parser.add_argument("--workers", type=int, default=4, help="并发线程数，默认 4")
    args = parser.parse_args()

    docs_dir = ROOT / "docs" / "swift"
    manifest_path = STATE_DIR / "swift.manifest.json"
    index_path = STATE_DIR / "swift.INDEX.md"

    print(f"来源: swift docs | 站点: {BASE_URL} | 线程: {args.workers}")

    pages = fetch_page_list()
    n_md = sum(1 for p in pages if p["ext"] == "md")
    print(f"searchindex.js 共 {len(pages)} 页（{n_md} md + {len(pages) - n_md} rst）\n")

    old = {}
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", {})

    def download(page):
        content = fetch(page["src_url"])
        if content is None or not content.strip():
            return page, None, "下载失败"
        head = content.lstrip()[:200].lower()
        if head.startswith("<!doctype") or head.startswith("<html"):
            return page, None, "返回的是 HTML 而不是源文件"
        return page, content, ""

    new_files = {}
    n_new = n_updated = n_unchanged = n_failed = 0
    failures = []

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, (page, content, err) in enumerate(pool.map(download, pages), 1):
            print(f"[{i}/{len(pages)}] {page['title']} ({page['docname']})")
            if err:
                print(f"    FAILED: {err}")
                failures.append(page)
                n_failed += 1
                continue

            out_path = docs_dir / f"{page['docname']}.{page['ext']}"
            rel = out_path.relative_to(ROOT).as_posix()
            sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
            group = page["docname"].split("/")[0] if "/" in page["docname"] else "(根目录)"
            new_files[page["url"]] = {
                "path": rel,
                "title": page["title"],
                "source_url": page["src_url"],
                "format": page["ext"],
                "group": group,
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

    lines = ["# ms-swift 中文文档索引", "",
             f"共 {len(new_files)} 页，同步时间: {datetime.now().isoformat(timespec='seconds')}"]
    cur_group = None
    for info in new_files.values():
        if info["group"] != cur_group:
            cur_group = info["group"]
            lines.append(f"\n## {cur_group}\n")
        fmt = " (RST)" if info["format"] == "rst" else ""
        lines.append(f"- [{info['title']}](../{info['path']}){fmt}")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    manifest_path.write_text(json.dumps({
        "source": "swift.docs",
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
            print(f"  - {p['title']} ({p['src_url']})")
        sys.exit(1)


if __name__ == "__main__":
    main()
