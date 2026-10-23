#!/usr/bin/env python3
"""validate_structure.py — 校验一个学习领域目录的产出物结构完整性。

用法: validate_structure.py <learning目录，如 ./learning/ops-dba>
退出码: 0=通过(允许警告)，1=有错误
"""
import re
import sys
from pathlib import Path

CURRENT_SCHEMA = 1
VALID_NOTE_STATUS = {"learning", "done", "review", "mastered"}
VALID_ROADMAP_STATUS = ("🔲", "🔵", "✅", "⚠️", "⏭️")


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def check_schema(path: Path, errors: list, warns: list) -> None:
    fm = frontmatter(path.read_text(encoding="utf-8"))
    m = re.search(r"schema_version:\s*(\d+)", fm)
    if not m:
        errors.append(f"{path.name}: frontmatter 缺少 schema_version")
        return
    v = int(m.group(1))
    if v > CURRENT_SCHEMA:
        errors.append(f"{path.name}: schema_version={v} 高于当前支持的 {CURRENT_SCHEMA}，请升级 skill")
    elif v < CURRENT_SCHEMA:
        warns.append(f"{path.name}: schema_version={v} 低于当前版本，需按 state-schema.md 迁移")


def check_roadmap(path: Path, errors: list) -> None:
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        cells = [c.strip() for c in line.split("|")]
        # 模块表数据行：首列为数字
        if len(cells) >= 6 and cells[1].isdigit():
            status = cells[4]
            if not any(s in status for s in VALID_ROADMAP_STATUS):
                errors.append(f"roadmap.md 第{i}行: 非法状态值 '{status}'（合法: {'/'.join(VALID_ROADMAP_STATUS)}）")


def check_notes(root: Path, errors: list, warns: list) -> None:
    notes_dir = root / "notes"
    if not notes_dir.is_dir():
        warns.append("缺少 notes/ 目录（P4 未开始可忽略）")
        return
    for p in sorted(notes_dir.glob("*.md")):
        if not re.match(r"^\d{2}-", p.stem):
            warns.append(f"notes/{p.name}: 文件名缺两位序号前缀（规范: <序号>-<模块slug>.md，序号=roadmap #）")
        fm = frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            errors.append(f"notes/{p.name}: 缺少 YAML frontmatter")
            continue
        m = re.search(r"status:\s*(\w+)", fm)
        if not m:
            errors.append(f"notes/{p.name}: frontmatter 缺少 status")
        elif m.group(1) not in VALID_NOTE_STATUS:
            errors.append(f"notes/{p.name}: 非法 status '{m.group(1)}'（合法: {'/'.join(sorted(VALID_NOTE_STATUS))}）")
        for field in ("domain", "module", "review_due"):
            if not re.search(rf"{field}:", fm):
                warns.append(f"notes/{p.name}: frontmatter 建议补充字段 {field}")


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit("用法: validate_structure.py <learning目录，如 ./learning/ops-dba>")
    root = Path(sys.argv[1])
    if not root.is_dir():
        sys.exit(f"目录不存在: {root}")

    errors: list = []
    warns: list = []

    for f in ("profile.md", "roadmap.md"):
        if not (root / f).exists():
            errors.append(f"缺少必需文件: {f}")
    if not (root / "knowledge-map.md").exists():
        warns.append("缺少 knowledge-map.md（P2 未开始可忽略）")

    for f in ("profile.md", "roadmap.md"):
        p = root / f
        if p.exists():
            check_schema(p, errors, warns)
    if (root / "roadmap.md").exists():
        check_roadmap(root / "roadmap.md", errors)
    check_notes(root, errors, warns)

    for w in warns:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}")
    print(f"\n校验结果: {len(errors)} 个错误, {len(warns)} 个警告 → {'FAIL' if errors else 'PASS'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
