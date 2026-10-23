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
- 读到的版本低于当前版本时，先按迁移规则升级再写入；高于当前版本时停止写入并提示用户 skill 需要升级。
- 迁移规则：v1 为首版，暂无迁移逻辑；后续版本变更在此追加说明。

## 各文件关键字段

### profile.md（frontmatter）

| 字段 | 含义 |
|---|---|
| `schema_version` | 固定 1 |
| `domain` / `subdomain` | 领域 / 细分 |
| `goal_level` | `aware`（了解）/ `usable`（能用）/ `master`（精通） |
| `baseline` | 现有基础描述 |
| `time_budget` | 每周可投入时长 |
| `created` / `updated` | 日期（YYYY-MM-DD） |

### roadmap.md（模块状态表）

- 每个模块一行：`| 模块 | 前置 | 状态 | 掌握证据 | 笔记链接 |`
- 状态枚举：`🔲 未开始` / `🔵 进行中` / `✅ 已完成` / `⚠️ 需复习` / `⏭️ 跳过`
- **roadmap.md 是进度的唯一权威来源**，任何进度变化必须更新它，不得只在对话中口头记录。

## 一致性规则 [MUST]

- 写状态文件前确认路径与 schema_version 正确。
- 同一信息只存一处（如模块状态只在 roadmap.md，笔记 frontmatter 的 `status` 与其保持同步）。
- 发现两处不一致时，以 roadmap.md 为准修正另一处，并在 review-log.md 记录。
