# 旧学习目录迁移说明（schema v1）

用于把旧版学习目录对齐到当前状态规则。迁移前先备份目录；迁移时不覆盖笔记正文、不改路线顺序。

## 1. 以路线表为准核对笔记状态

逐行检查 `roadmap.md`，按下表更新对应笔记 frontmatter 的 `status`：

| 路线表状态 | 笔记状态 | 适用情况 |
|---|---|---|
| `🔲 未开始` | `planned` | 只有空骨架，尚未开始学习 |
| `🔵 进行中` | `learning` | 正在学习或已经填入学习记录 |
| `✅ 已完成` | `done` 或 `mastered` | 已完成但仍在复习用 `done`；完成全部复习轮次用 `mastered` |
| `⚠️ 需复习` | `review` | 已到复习日期或上次复习未通过 |
| `⏭️ 跳过` | 可无笔记 | 路线表为权威来源；保留既有笔记时不要求更改正文 |

旧笔记一律标成 `learning` 的情况，不应机械批量改名：先根据路线表和笔记内容判断；空骨架且路线为未开始时改为 `planned`，真实进行中的笔记保留 `learning`。

## 2. 补齐复习字段

`done` 与 `review` 笔记需要：

```yaml
review_due: YYYY-MM-DD
review_stage: 1
```

如果无法确认旧复习记录，不要推测已通过轮次。经用户确认从第一轮重新开始后，将轮次设为 1，并从迁移当天起按 `review.md` 重新排期。旧字段 `passes_in_stage` 可删除或保留作历史记录；新版默认复习规则不再使用它。尚未确定复习日期时可暂填 `review_due: null`，并在下一次续学时确认；不要伪造历史日期。`mastered` 笔记设 `review_due: null`。

## 3. 核对状态版本与目录

- `profile.md` 和 `roadmap.md` 必须有 `schema_version: 1`；其他状态文件不添加该字段。
- 确认 `profile.md` 的 `domain`、`subdomain` 能唯一识别该学习目录。
- 确认路线表中的笔记链接、文件序号及模块状态相符。
- 对照 `references/core/review.md` 修正到期复习项。

迁移完成后运行：

```bash
scripts/validate_structure.py ./learning/<领域slug>
```
