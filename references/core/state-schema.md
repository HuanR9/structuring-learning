# 状态文件 Schema（读写前必读）

## 目录结构

```
./learning/<领域slug>/
├── profile.md          # 学习者档案（P0 产出）
├── research-notes.md   # 调研记录（P1 产出，可选）
├── knowledge-map.md    # 知识地图（P2 产出）
├── roadmap.md          # 学习路径（P3 产出，进度唯一权威来源）
├── notes/              # 模块笔记（P4）
│   └── <序号>-<模块slug>.md
└── review-log.md       # 复盘日志（P5，追加写）
```

## 命名规则

- **领域slug**：`<L1领域>-<细分>` 小写连字符，如 `ops-dba`、`dev-backend`。无细分时只用领域名。
- **模块slug**：模块名英文化小写连字符，如 `innodb-storage`；无法英文化时用拼音。
- **笔记文件**：`notes/<两位序号>-<模块slug>.md`，序号取 `roadmap.md` 模块表 `#` 列（重排联动规则见 `notes.md`）。

## schema_version

- 当前版本：`1`。
- `profile.md` 与 `roadmap.md` 的 YAML frontmatter [MUST] 含 `schema_version: 1`。
- `knowledge-map.md`、`research-notes.md`、`notes/*.md` 与 `review-log.md` 不使用 `schema_version`；它们按各自内容规范维护。
- 读到的版本低于当前版本时，先按迁移规则升级再写入；高于当前版本时停止写入并提示用户 skill 需要升级。
- Schema 字段的版本迁移规则：v1 为首版，目前没有旧 schema 的自动迁移；后续版本变更在此追加说明。
- 旧学习目录的状态与复习字段人工迁移见 `references/core/migration-v1.md`。

## 各文件关键字段

### profile.md（frontmatter）

| 字段 | 含义 |
|---|---|
| `schema_version` | 固定 1 |
| `domain` / `subdomain` | 领域 / 细分 |
| `goal_level` | `aware`（了解）/ `usable`（能用）/ `master`（精通） |
| `baseline` | 现有基础描述 |
| `time_budget` | 每周可投入时长 |
| `jurisdiction` | 法律、监管等强辖区差异主题的适用国家/地区；其他主题可省略 |
| `created` / `updated` | 日期（YYYY-MM-DD） |

### research-notes.md（P1 调研记录）

按 `templates/research-notes.md` 逐条记录信源。每条至少包含来源名称、可访问链接或书目信息、适用领域/版本/司法辖区、核对日期，以及该来源支持的具体结论；无法确认的发布日期或适用范围明确写“未确认”，不得猜测。

### roadmap.md（模块状态表）

- 每个模块一行：`| 模块 | 前置 | 状态 | 掌握证据 | 笔记链接 |`
- `前置` 填 `无` 或逗号分隔的模块编号（如 `#1, #2`）；依赖必须指向存在的模块，且不能形成循环。
- 状态枚举：`🔲 未开始` / `🔵 进行中` / `✅ 已完成` / `⚠️ 需复习` / `⏭️ 跳过`
- **roadmap.md 是进度的唯一权威来源**，任何进度变化必须更新它，不得只在对话中口头记录。
- 笔记状态与路线表映射：`planned` → `🔲`；`learning` → `🔵`；`done` 与 `mastered` → `✅`；`review` → `⚠️`。路线表为权威来源，笔记状态是同步副本；`⏭️` 模块不要求保留笔记。
- `done` / `review` 笔记用 `review_stage` 记录复习轮次；`passes_in_stage` 是旧版可选字段，新建笔记不需要它。

## 一致性规则 [MUST]

- 写状态文件前确认路径与 schema_version 正确。
- 同一信息只存一处（如模块状态只在 roadmap.md，笔记 frontmatter 的 `status` 与其保持同步）。
- 发现两处不一致时，以 roadmap.md 为准修正另一处，并在 review-log.md 记录。

## 隐私与敏感材料边界

- 不把密码、访问令牌、私钥、Cookie、个人身份信息或完整的机密内部文档写入学习状态文件。
- 学习确需使用受限材料时，只记录脱敏后的必要结论、材料标题和用户可访问的位置；不要把原文复制到 `research-notes.md`。
- 未经用户明确要求，不把学习状态或内部材料发送到外部服务；使用联网信源时只查询完成任务所需的最少信息。
