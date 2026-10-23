#!/bin/bash
# sync-to-workbuddy.sh — 将本仓库（权威源）同步到 WorkBuddy 工具内 skill 目录
#
# 用法：
#   ./scripts/sync-to-workbuddy.sh            # 权威源 → 工具内（默认方向）
#   ./scripts/sync-to-workbuddy.sh --dry-run  # 只预览差异，不实际写入
#
# 注意：工具内目录是纯副本（不含学习产出物，产出物在各自项目的 learning/ 下），
#       因此使用 --delete 保证两边严格一致。

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$HOME/.workbuddy/skills/structuring-learning"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "目标目录不存在: ${TARGET_DIR}" >&2
  echo "请确认 WorkBuddy 已安装且用户级 skills 目录存在。" >&2
  exit 1
fi

echo "源: ${REPO_DIR}"
echo "目标: ${TARGET_DIR}"
if [[ -n "$DRY_RUN" ]]; then
  echo "模式: dry-run（仅预览）"
else
  echo "模式: 实际同步（--delete）"
fi
echo

rsync -a --delete --exclude=".DS_Store" $DRY_RUN \
  "$REPO_DIR/" "$TARGET_DIR/"

if [[ -z "$DRY_RUN" ]]; then
  echo
  echo "同步完成。建议在 WorkBuddy 新开会话验证 skill 生效。"
fi
