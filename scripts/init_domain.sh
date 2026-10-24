#!/usr/bin/env bash
# init_domain.sh — 初始化一个学习领域的状态目录骨架
# 用法: init_domain.sh <领域slug> [学习根目录，默认当前目录]
# 示例: init_domain.sh ops-dba            → ./learning/ops-dba/
#       init_domain.sh dev-backend /path  → /path/learning/dev-backend/
set -euo pipefail

SLUG="${1:?用法: init_domain.sh <领域slug> [学习根目录]}"
ROOT="${2:-.}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$ROOT/learning/$SLUG"
TODAY="$(date +%F)"

# slug 合法性：小写字母/数字/连字符
if [[ ! "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "非法 slug: ${SLUG}（仅允许小写字母、数字、连字符）" >&2
  exit 1
fi

if [[ -d "$TARGET" ]]; then
  echo "目录已存在，拒绝覆盖: $TARGET" >&2
  exit 1
fi

mkdir -p "$TARGET/notes"

sed -e "s/YYYY-MM-DD/$TODAY/g" "$SKILL_DIR/templates/domain-profile.md" > "$TARGET/profile.md"
sed -e "s/YYYY-MM-DD/$TODAY/g" -e "s/<领域slug>/$SLUG/g" "$SKILL_DIR/templates/roadmap.md" > "$TARGET/roadmap.md"
cp "$SKILL_DIR/templates/knowledge-map.md" "$TARGET/knowledge-map.md"

cat > "$TARGET/review-log.md" <<EOF
# 复盘日志：$SLUG

> 追加写，不覆盖。每条含日期、结论、触发的文件变更清单。
EOF

echo "已初始化: $TARGET"
echo "请先填写 profile.md 与 roadmap.md 中的占位信息，再运行 validate_structure.py。"
find "$TARGET" -type f | sort
