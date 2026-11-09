# -*- coding: utf-8 -*-
"""
llm-docs-mirror 唯一同步入口：一条命令把 5 个来源全部刷到最新，并自动 commit。

设计：
- SOURCES 表是「框架 → 平台适配器 → 输出目录」的唯一权威映射；
  新增框架时只加一行（若为新平台才需要新增适配器）。
- 没有"只跑某个来源"的跳过参数：每次运行 5 个都会跑，保证不会漏更新。
- 单个来源失败不阻断其它来源，结尾汇总 OK/FAILED 与用时。
- 跑完自动 git commit（--no-commit 可关），于是 git log / git diff 就是
  官方文档的变更历史：能回答"某一周 GRPO 文档改了哪几段"。

用法：
  python sync_all.py
  python sync_all.py --no-commit
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 框架, 类型, 平台适配器, 输出目录, 传给适配器的参数
SOURCES = [
    ("trl",          "docs",     "hf_docs.py",        "docs/trl",         ["trl"]),
    ("trl",          "releases", "github_releases.py", "releases/trl",     ["huggingface/trl"]),
    ("transformers", "docs",     "hf_docs.py",        "docs/transformers", ["transformers"]),
    ("unsloth",      "docs",     "gitbook_docs.py",   "docs/unsloth",     []),
    ("swift",        "docs",     "sphinx_docs.py",    "docs/swift",       []),
]


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args),
                          capture_output=True, text=True)


def auto_commit():
    if not (ROOT / ".git").exists():
        print("（未发现 .git，跳过自动 commit）")
        return
    git("add", "-A")
    status = git("status", "--porcelain")
    if not status.stdout.strip():
        print("（无文件变更，跳过 commit）")
        return
    changed = len([l for l in status.stdout.splitlines() if l.strip()])
    msg = f"sync: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {changed} files changed"
    r = git("commit", "-m", msg)
    if r.returncode == 0:
        print(f"自动 commit 完成: {msg}")
        head = git("rev-parse", "--short", "HEAD")
        print(f"  commit: {head.stdout.strip()}")
    else:
        print(f"自动 commit 失败: {r.stderr.strip() or r.stdout.strip()}")


def main():
    parser = argparse.ArgumentParser(description="同步全部文档来源并自动 commit")
    parser.add_argument("--no-commit", action="store_true", help="跑完不自动 git commit")
    args = parser.parse_args()

    print(f"同步全部 {len(SOURCES)} 个来源 | 仓库: {ROOT}\n")
    results = []
    total_start = time.time()

    for framework, kind, adapter, output, extra in SOURCES:
        script = ROOT / "crawlers" / adapter
        if not script.exists():
            print(f"[跳过-脚本不存在] {framework} {kind}: {script}")
            results.append((f"{framework} {kind}", "脚本不存在"))
            continue
        label = f"{framework} {kind}"
        print("=" * 60)
        print(f">>> {label}  ({adapter} {' '.join(extra)})  ->  {output}")
        print("=" * 60)
        start = time.time()
        proc = subprocess.run([sys.executable, str(script)] + extra)
        elapsed = int(time.time() - start)
        status = "OK" if proc.returncode == 0 else f"FAILED (exit {proc.returncode})"
        results.append((label, f"{status}, 用时 {elapsed}s"))
        print(f"<<< {label}: {status}, 用时 {elapsed}s\n")

    print("=" * 60)
    print(f"全部完成，总用时 {int(time.time() - total_start)}s")
    for label, status in results:
        print(f"  {label}: {status}")

    if not args.no_commit:
        print()
        auto_commit()

    if any("FAILED" in s or "不存在" in s for _, s in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
