# llm-docs-mirror

## 1. 这个仓库是干什么的

把 **4 个框架 / 5 个来源**的官方文档与更新日志抓成本地 markdown 镜像，并用 git 记录它们的演进。

- 文档会实时更新（TRL 约每周发一版），**重复运行一条命令即可同步到最新**；
- 每次同步后自动 commit，于是 `git log` / `git diff` 就是官方 changelog，
  能回答"v1.17 那一周 GRPO 文档改了哪几段"；
- 目录结构尽量**与官网一致且有序**：一级章节名与官网侧边栏一一对应，
  前缀两位序号按官网 `chapters` 顺序自动生成，打开文件夹就能按官网顺序读。

## 2. 来源一览（唯一权威映射在 `sync_all.py` 的 `SOURCES` 表）

| # | 框架 | 类型 | 官网 | 平台适配器 | 输出目录 | 条目数 |
|---|---|---|---|---|---|---|
| 1 | trl | 文档 | `huggingface.co/docs/trl` | `crawlers/hf_docs.py` | `docs/trl/` | 57 |
| 2 | trl | 更新日志 | `github.com/huggingface/trl/releases` | `crawlers/github_releases.py` | `releases/trl/` | 103 |
| 3 | transformers | 文档 | `huggingface.co/docs/transformers` | `crawlers/hf_docs.py` | `docs/transformers/` | 774 |
| 4 | unsloth | 文档 | `unsloth.ai/docs` | `crawlers/gitbook_docs.py` | `docs/unsloth/` | 201 |
| 5 | ms-swift | 文档（中文） | `swift.readthedocs.io/zh-cn/latest` | `crawlers/sphinx_docs.py` | `docs/swift/` | 75 |

合计 1210 个条目。

`sync_all.py` 顶部那张表既是文档也是执行清单，不会和代码脱节：

```python
SOURCES = [
    ("trl",          "docs",     "hf_docs.py",        "docs/trl",         ["trl"]),
    ("trl",          "releases", "github_releases.py", "releases/trl",     ["huggingface/trl"]),
    ("transformers", "docs",     "hf_docs.py",        "docs/transformers", ["transformers"]),
    ("unsloth",      "docs",     "gitbook_docs.py",   "docs/unsloth",     []),
    ("swift",        "docs",     "sphinx_docs.py",    "docs/swift",       []),
]
```

## 3. 新框架该用哪个适配器（识别决策表）

代码按**平台**分脚本，不按框架分包——因为 trl 和 transformers 共用一套 HF 文档站机制，
按框架拆会逼出复制代码或公共抽象层。新增框架时按下面特征判断：

| 打开官网看到 | 用哪个适配器 |
|---|---|
| 页面源码有 `data-target="SideMenu"`，且每页 URL 加 `.md` 能拿到 markdown 原文 | `crawlers/hf_docs.py` |
| 有 `/llms.txt`，里面全是 `.md` 链接 | `crawlers/gitbook_docs.py` |
| 有 `/searchindex.js` + `/_sources/*.md.txt` | `crawlers/sphinx_docs.py` |
| 目标是 `github.com/<owner>/<repo>/releases` | `crawlers/github_releases.py` |

加框架时通常只需在 `SOURCES` 加一行；只有出现全新的文档平台才需要写新适配器。

## 4. 目录结构

```
llm-docs-mirror/
├── .git/
├── .gitignore
├── README.md
├── sync_all.py                  # 唯一入口：跑 5 个来源 + 自动 commit
├── requirements.txt
├── crawlers/                    # 4 个平台适配器（代码按平台分）
│   ├── hf_docs.py               # → trl、transformers
│   ├── github_releases.py       # → trl releases
│   ├── gitbook_docs.py          # → unsloth
│   └── sphinx_docs.py           # → ms-swift
├── state/                       # 非官网元数据（全部提交进 git）
│   ├── *.manifest.json          # URL 主键的增量状态（每页 sha256 + 落盘路径）
│   ├── *.SUMMARY.md             # HF 系章节索引
│   └── *.INDEX.md               # GitBook / Sphinx / Releases 索引
├── docs/                        # 纯官网文档镜像，按框架分
│   ├── trl/          00_getting_started/ … 07_experimental/
│   ├── transformers/ 00_get_started/ … 08_api/{main_classes, models/text_models, …}/
│   ├── unsloth/      docs.md  desktop.md  get-started/install/  models/  blog/ …
│   └── swift/        index.rst  GetStarted/  Instruction/GRPO/...  BestPractices/ …
└── releases/
    └── trl/          v0.2.0.md … v1.17.1.md
```

**为什么 `SUMMARY.md` / `INDEX.md` / `manifest.json` 不在 `docs/` 里**：
它们是本仓库加的元数据，官网没有。放进文档树会破坏"纯镜像"，
所以统一集中在 `state/`，索引里的链接用 `../docs/...` 指回文档。

**为什么 unsloth / swift / releases 没有编号前缀**：
它们的官网 URL 本身就带层级（或天然按版本时间排序），硬塞序号反而破坏一致性；
顺序交给各自的 `INDEX.md`。

## 5. 目录与官网"一致且有序"是怎么做到的

`hf_docs.py` 解析官网 index 页内嵌的 `SideMenu` JSON 后，按 `chapters` 出现顺序
`enumerate` 生成目录名：

```python
chapter_dir = f"{idx:02d}_{slugify(chapter['title'])}"
```

- 序号**不写死**：官网改组章节时自动跟随，不会出现"编号和实际顺序对不上"；
- `slugify` 只做文件名安全化（空格/连字符→下划线、小写），章节名与官网一一对应；
- 嵌套子分组（`API > Utilities`、`API > Models > Text models`）照抄为子目录，不加序号；
- 文件名用官网页面 URL 的最后一段（如 `sft_trainer.md`），内容是官方 markdown 原文。

例子：官网 `Getting started > Installation` → `00_getting_started/installation.md`；
官网 `API > Models > Text models > CANINE` → `08_api/models/text_models/canine.md`。

## 6. 快速开始

```bash
# 安装依赖（只有 requests）
pip install -r requirements.txt

# 同步全部 5 个来源（每次都会全跑，跑完自动 commit）
python sync_all.py

# 只同步不 commit
python sync_all.py --no-commit

# 单独跑某个适配器（调试用；注意这样其它来源不会更新）
python crawlers/hf_docs.py trl
python crawlers/hf_docs.py transformers --workers 3 --force
python crawlers/gitbook_docs.py --workers 8
python crawlers/sphinx_docs.py --workers 4
python crawlers/github_releases.py huggingface/trl
```

## 7. 参数说明

| 适配器 | 参数 | 默认值 | 说明 |
|---|---|---|---|
| 全部 | `--force` | 关 | 强制重写所有文件；默认内容 sha256 没变就不落盘 |
| `hf_docs.py` | `library` | 必填 | `trl` 或 `transformers` |
| `hf_docs.py` | `--base-url` | `https://hf-mirror.com` | 代理稳定时可换 `https://huggingface.co` |
| `hf_docs.py` | `--workers` | `3` | 官方 CDN 按 IP 限流，不建议超过 4 |
| `gitbook_docs.py` | `--workers` | `8` | GitBook 未观察到限流 |
| `sphinx_docs.py` | `--workers` | `4` | Read the Docs 未观察到限流 |
| `github_releases.py` | `repo` | 必填 | `owner/repo` |
| `sync_all.py` | `--no-commit` | 关 | 跑完不自动 git commit |

环境变量 `GITHUB_TOKEN`：设置后 GitHub API 限额从 60 次/小时提升到 5000 次/小时。

## 8. 增量更新机制（应对"文档实时更新"）

每次运行 `sync_all.py`：

1. **重新拉页面清单** —— HF 的 SideMenu JSON、GitBook 的 `llms.txt`、
   Sphinx 的 `searchindex.js`、GitHub Releases API 全部重新请求，
   官网新增/删除页面自动跟随；
2. **重新下载每一页正文**，逐条对比 sha256：变了才写盘（`NEW` / `UPDATED`），
   没变跳过（`unchanged`），文件修改时间即"内容最后变化时间"；
3. **官网已删除的页面**本地保留不删，只在结尾报告；
4. **manifest 以页面官方 URL 为主键**（不是相对路径）。这是关键设计：
   官网改组章节导致目录 rename 时，sha256 记录不会失效，
   不会把上千页误判成"新页面"全部重写。
   key 形如 `https://huggingface.co/docs/trl/index`（不含 `.md`，与实际下载用的
   `.md` 端点区分），值里的 `path` 记录落盘位置；因为 key 本身已是 URL，
   记录里不再重复存 `url` 字段；
5. 请求一律带 `Cache-Control: no-cache`，避免镜像/CDN 返回旧副本被误判成"没更新"；
6. 跑完 `git add -A` + `git commit`（无变更则跳过）。

## 9. 变更历史怎么看

```bash
git log --oneline                          # 每次同步就是一个 commit
git show <commit> --stat                   # 这一周哪些页变了
git diff <old> <new> -- docs/trl/02_trainers/grpo_trainer.md
```

`state/*.manifest.json` 记录每页 hash，也提交进 git，所以 diff 里能同时看到
"哪些页内容变了"和"目录结构怎么变了"。

## 10. 网络与限流（实测结论，2026-11-09）

| 站点 | 情况 |
|---|---|
| `api.github.com` | 国内直连可达；匿名 60 次/小时按 IP 计，403 时脚本按 `X-RateLimit-Reset` 自动等待重试 |
| `unsloth.ai` | 直连可达，无限流 |
| `swift.readthedocs.io` | 直连可达，无限流 |
| `hf-mirror.com` | 国内直连可达；但 transformers 的 `.md` 请求会 **308 跳回 huggingface.co** |
| `huggingface.co` CDN | **按 IP 约 0.3 请求/秒**。8 线程实测全部 HTTP 429 + `Retry-After: 127/42` |

所以 `hf_docs.py` 内置 429/503 的 `Retry-After` 退避重试（加随机错峰，最多 5 次），
`--workers` 默认 3（可改，但不建议超过 4）。Transformers 774 页实测约 38 分钟——
**这是站点限速决定的下限，堆线程只会更慢**。其它 4 个来源合计约 3 分钟。
注意"未变"也必须把每页正文重新下载一遍才能算 sha256，所以即便官网一篇没改，
Transformers 这一项也不会变快。

## 11. 常见问题

**Q: `sync_all.py` 卡住十几分钟没动？**
大概率是 GitHub API 匿名配额耗尽，脚本在等 `X-RateLimit-Reset`（最多 1 小时）。
设置 `GITHUB_TOKEN` 可避免。Transformers 那一项本身就要约 38 分钟，属正常。

**Q: `FATAL: 页面里找不到 SideMenu JSON`？**
HuggingFace 改了文档站结构，需更新 `crawlers/hf_docs.py` 的 `fetch_sidebar_pages()`。

**Q: `FATAL: llms.txt 里没有解析到页面链接`？**
GitBook 改了行格式，更新 `crawlers/gitbook_docs.py` 顶部的 `LINK_RE`。

**Q: `FATAL: searchindex.js 三个数组长度不一致`？**
Sphinx 升级改了索引格式，更新 `crawlers/sphinx_docs.py` 的 `fetch_page_list()`。

**Q: 个别页 `FAILED: 返回的是 HTML 而不是 markdown`？**
站点瞬时抖动或该页没有 `.md` 端点。脚本会继续爬其它页并在结尾列失败清单，
重跑一次即可补上（增量机制会跳过未变页面）。

**Q: 为什么 swift 有 `.rst` 文件？**
那是 Sphinx 的 toctree 目录索引页，官网源文件本身就是 RST；内容页基本都是 `.md`。
脚本按 `searchindex.js` 里 `filenames` 的真实后缀落盘，不把 RST 冒充 markdown。

## 附录 A：迁移记录（2026-11-09）

统一前是 5 个独立项目：`trl-transformers-docs-crawler`、`trl-releases-crawler`、
`unsloth-docs-crawler`、`swift-docs-crawler`、`docs-sync-all`。
迁移时用 `robocopy /E` 复制数据（整目录 `mv` 会被宿主句柄拒绝），
逐文件 md5 校验 5 个来源全部一致；旧 manifest 转换成 URL 主键格式放入 `state/`；
transformers 的 `00_getting_started` 按官网章节名 "Get started" 改为 `00_get_started`。
旧项目目录原地保留作为历史快照，本仓库 `sync_all.py` 是此后唯一的维护入口。

## 附录 B：为什么修过 SUMMARY.md

旧版 `crawl_hf_docs.py` 生成索引时，拼的相对路径是相对 `docs/<lib>/` 的，
而 manifest 的 key 是相对项目根的 `docs/<lib>/...`，前缀不匹配导致
所有页面被当成"失败"跳过，两个 SUMMARY.md 里 **0 个链接**。
现在索引统一由 `state/` 生成并用 manifest 里的 `path` 字段，
链接形如 `../docs/trl/00_getting_started/index.md`。

## 附录 C：URL 主键曾拼出重复前缀（2026-11-09 修复）

迁移旧 manifest 时，把 `page["url_path"]` 当成"页面相对路径"又拼了一次库名前缀：

```python
# 错误：url_path 本身已是 /docs/trl/index，再拼会变成 /docs/trl/docs/trl/index
official_url = f"https://huggingface.co/docs/{lib}{page['url_path']}"
# 正确
official_url = "https://huggingface.co" + page["url_path"]
```

结果 `state/trl.manifest.json` 的 57 条、`state/transformers.manifest.json` 的 774 条
key 全部形如 `https://huggingface.co/docs/trl/docs/trl/index`。

**这个 bug 很隐蔽**：key 仍然唯一、仍然能正常做增量判断（脚本里两处拼接用了同一个
错误公式，读写自洽），所以同步结果一直是 `unchanged`，不会报错；只是 manifest 里记的
URL 打不开，且以后若按真实 URL 去查表就会查不到。

修复分两步，缺一不可：

1. 改 `crawlers/hf_docs.py` 的**两处**生成逻辑（主下载循环 + SUMMARY 生成循环）；
2. 把 `state/*.manifest.json` 里已落盘的旧 key 批量改写，否则脚本一跑会把
   全部 831 页判成 `NEW` 并重写一遍。

修完复验：`hf_docs.py trl` → `0 新增, 0 更新, 57 未变, 0 失败`，且没有误报
"官网已删除"，说明新旧 key 完全对齐。
