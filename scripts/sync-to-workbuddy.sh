#!/bin/bash
# sync-to-workbuddy.sh — 将本仓库（权威源）同步到 WorkBuddy 工具内 skill 目录
#
# 用法：
#   ./scripts/sync-to-workbuddy.sh                 # 只预览差异（默认）
#   ./scripts/sync-to-workbuddy.sh --apply         # 实际同步，不删除目标独有文件
#   ./scripts/sync-to-workbuddy.sh --apply --prune # 同步并删除目标独有文件
#
# 默认保护目标中的 learning/ 用户数据。--prune 仅在明确指定时删除源中不存在的文件。

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$HOME/.workbuddy/skills/structuring-learning"

MODE="dry-run"
PRUNE="false"
APPLY_SEEN="false"
DRY_RUN_SEEN="false"
for arg in "$@"; do
  case "$arg" in
    --dry-run)
      [[ "$APPLY_SEEN" == "true" || "$DRY_RUN_SEEN" == "true" ]] && { echo "--dry-run 与 --apply 不能重复或同时使用" >&2; exit 2; }
      MODE="dry-run"
      DRY_RUN_SEEN="true"
      ;;
    --apply)
      [[ "$MODE" == "apply" || "$DRY_RUN_SEEN" == "true" ]] && { echo "--dry-run 与 --apply 不能重复或同时使用" >&2; exit 2; }
      MODE="apply"
      APPLY_SEEN="true"
      ;;
    --prune)
      PRUNE="true"
      ;;
    --help|-h)
      sed -n '4,9p' "$0"
      exit 0
      ;;
    *)
      echo "未知参数: $arg" >&2
      echo "用法: $0 [--dry-run | --apply] [--prune]" >&2
      exit 2
      ;;
  esac
done

if [[ "$PRUNE" == "true" && "$MODE" != "apply" ]]; then
  echo "--prune 只能与 --apply 一起使用" >&2
  exit 2
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "目标目录不存在: ${TARGET_DIR}" >&2
  echo "请确认 WorkBuddy 已安装且用户级 skills 目录存在。" >&2
  exit 1
fi

if [[ -L "$TARGET_DIR" ]]; then
  echo "目标目录是符号链接，拒绝同步: ${TARGET_DIR}" >&2
  exit 1
fi

echo "源: ${REPO_DIR}"
echo "目标: ${TARGET_DIR}"
if [[ "$MODE" == "dry-run" ]]; then
  echo "模式: 仅预览（不会写入）"
else
  echo "模式: 实际同步"
fi
if [[ "$PRUNE" == "true" ]]; then
  echo "清理: 删除目标中源仓库不存在的文件"
else
  echo "清理: 保留目标独有文件"
fi
echo "保护: learning/、.git/、.DS_Store"
echo

RSYNC_ARGS=(-a --itemize-changes --exclude='/.DS_Store' --exclude='/.git/' --exclude='/learning/')
if [[ "$MODE" == "dry-run" ]]; then
  RSYNC_ARGS+=(--dry-run)
fi
if [[ "$PRUNE" == "true" ]]; then
  RSYNC_ARGS+=(--delete)
fi

rsync "${RSYNC_ARGS[@]}" "$REPO_DIR/" "$TARGET_DIR/"

if [[ "$MODE" == "apply" ]]; then
  echo
  echo "同步完成。建议在 WorkBuddy 新开会话验证 skill 生效。"
fi
