#!/usr/bin/env python3
"""validate_structure.py — 校验一个学习领域目录的产出物结构完整性。

用法: validate_structure.py <learning目录，如 ./learning/ops-dba>
退出码: 0=通过(允许警告)，1=有错误
"""
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

CURRENT_SCHEMA = 1
VALID_NOTE_STATUS = {"planned", "learning", "done", "review", "mastered"}


def frontmatter(text: str) -> str:
    m = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    return m.group(1) if m else ""


def field_value(fm: str, name: str) -> Optional[str]:
    m = re.search(rf"^{re.escape(name)}:\s*(.*?)\s*$", fm, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"\'')


def is_placeholder(value: Optional[str]) -> bool:
    return value is None or not value or (value.startswith("<") and value.endswith(">"))


def valid_date(value: Optional[str]) -> bool:
    if value is None or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


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


ROADMAP_STATUSES = {
    "🔲": "未开始",
    "🔵": "进行中",
    "✅": "已完成",
    "⚠️": "需复习",
    "⏭️": "跳过",
}
NOTE_TO_ROADMAP = {"planned": "🔲", "learning": "🔵", "done": "✅", "mastered": "✅", "review": "⚠️"}


def roadmap_glyph(status: str) -> Optional[str]:
    for glyph, label in ROADMAP_STATUSES.items():
        if status == glyph or status == f"{glyph} {label}":
            return glyph
    return None


def parse_note_link(cell: str) -> Optional[str]:
    m = re.search(r"\[\[notes/([^]|#]+)", cell)
    if not m:
        return None
    target = m.group(1).strip()
    target = target if Path(target).suffix else f"{target}.md"
    return f"notes/{target}"


def check_roadmap(path: Path, errors: list) -> list:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not cells[0].isdigit():
            continue
        if len(cells) != 6:
            errors.append(f"roadmap.md 第{i}行: 模块表应有 6 列，实际为 {len(cells)} 列")
            continue
        status = cells[3]
        glyph = roadmap_glyph(status)
        if glyph is None:
            errors.append(f"roadmap.md 第{i}行: 非法状态值 '{status}'（合法状态: {' / '.join(f'{g} {label}' for g, label in ROADMAP_STATUSES.items())}）")
        if is_placeholder(cells[1]):
            errors.append(f"roadmap.md 第{i}行: 模块名称为空或仍是模板占位符")
        if is_placeholder(cells[4]):
            errors.append(f"roadmap.md 第{i}行: 缺少掌握证据或仍是模板占位符")
        if is_placeholder(cells[2]):
            errors.append(f"roadmap.md 第{i}行: 前置模块为空；无前置时填写“无”")
        dependencies = [int(n) for n in re.findall(r"#(\d+)", cells[2])]
        if int(cells[0]) in dependencies:
            errors.append(f"roadmap.md 第{i}行: 模块不能依赖自身")
        rows.append({"line": i, "number": int(cells[0]), "status": glyph, "note": parse_note_link(cells[5]), "dependencies": dependencies})
    if not rows:
        errors.append("roadmap.md: 未找到模块表数据行")
    numbers = [row["number"] for row in rows]
    if len(numbers) != len(set(numbers)):
        errors.append("roadmap.md: 模块编号重复")
    number_set = set(numbers)
    for row in rows:
        for dependency in row["dependencies"]:
            if dependency not in number_set:
                errors.append(f"roadmap.md 第{row['line']}行: 前置模块 #{dependency} 不存在")
    graph = {row["number"]: row["dependencies"] for row in rows}
    visiting, visited = set(), set()

    def visit(number: int) -> None:
        if number in visiting:
            errors.append(f"roadmap.md: 前置依赖存在循环（涉及模块 #{number}）")
            return
        if number in visited:
            return
        visiting.add(number)
        for dependency in graph.get(number, []):
            if dependency in graph:
                visit(dependency)
        visiting.remove(number)
        visited.add(number)

    for number in graph:
        visit(number)
    return rows


def check_profile(path: Path, errors: list, warns: list) -> None:
    fm = frontmatter(path.read_text(encoding="utf-8"))
    if not fm:
        errors.append("profile.md: 缺少 YAML frontmatter")
        return
    for field in ("domain", "subdomain", "goal_level", "baseline", "time_budget", "created", "updated"):
        value = field_value(fm, field)
        if is_placeholder(value):
            errors.append(f"profile.md: {field} 为空或仍是模板占位符")
    goal = field_value(fm, "goal_level")
    if goal and goal not in {"aware", "usable", "master"}:
        errors.append(f"profile.md: 非法 goal_level '{goal}'（合法: aware/usable/master）")
    for field in ("created", "updated"):
        value = field_value(fm, field)
        if value and not is_placeholder(value) and not valid_date(value):
            errors.append(f"profile.md: {field} 应为有效日期 YYYY-MM-DD")


def check_research_notes(path: Path, errors: list, warns: list) -> None:
    rows = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if "|" not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or not cells[0].isdigit():
            continue
        rows += 1
        labels = ("问题/主张", "来源名称与发布方", "链接/书目信息", "适用范围", "发布或生效日期", "核对日期", "支持的结论与局限")
        values = cells[1:]
        for label, value in zip(labels, values):
            if is_placeholder(value):
                errors.append(f"research-notes.md 第{line_number}行: {label} 为空或仍是模板占位符")
        if not is_placeholder(values[5]) and not valid_date(values[5]):
            errors.append(f"research-notes.md 第{line_number}行: 核对日期应为有效日期 YYYY-MM-DD")
        if values[3].strip('"\'') == "未确认":
            warns.append(f"research-notes.md 第{line_number}行: 尚未确认来源的适用范围")
        if values[4].strip('"\'') == "未确认":
            warns.append(f"research-notes.md 第{line_number}行: 尚未确认来源的发布日期或生效日期")
    if not rows:
        warns.append("research-notes.md: 未找到已填写的信源表格记录")


def check_notes(root: Path, errors: list, warns: list, roadmap_rows: list) -> None:
    notes_dir = root / "notes"
    if not notes_dir.is_dir():
        warns.append("缺少 notes/ 目录（P4 未开始可忽略）")
        return
    notes = {p.relative_to(root).as_posix(): p for p in notes_dir.glob("*.md")}
    linked_notes = set()
    roadmap_by_note = {}
    for row in roadmap_rows:
        if row["note"]:
            roadmap_by_note[row["note"]] = row
            linked_notes.add(row["note"])
            if row["note"] not in notes:
                warns.append(f"roadmap.md 第{row['line']}行: 笔记链接不存在: {row['note']}")

    for p in sorted(notes_dir.glob("*.md")):
        if not re.match(r"^\d{2}-", p.stem):
            warns.append(f"notes/{p.name}: 文件名缺两位序号前缀（规范: <序号>-<模块slug>.md，序号=roadmap #）")
        relative = p.relative_to(root).as_posix()
        m_number = re.match(r"^(\d{2})-", p.name)
        if m_number:
            matching = [row for row in roadmap_rows if row["number"] == int(m_number.group(1))]
            if not matching:
                warns.append(f"notes/{p.name}: 序号 {m_number.group(1)} 未出现在 roadmap.md")
            elif len(matching) == 1 and matching[0]["note"] and matching[0]["note"] != relative:
                errors.append(f"notes/{p.name}: 文件序号与 roadmap.md 第{matching[0]['line']}行的笔记链接不一致")
        fm = frontmatter(p.read_text(encoding="utf-8"))
        if not fm:
            errors.append(f"notes/{p.name}: 缺少 YAML frontmatter")
            continue
        m = re.search(r"^status:\s*(\w+)\s*$", fm, re.M)
        note_status = None
        if not m:
            errors.append(f"notes/{p.name}: frontmatter 缺少 status")
        elif m.group(1) not in VALID_NOTE_STATUS:
            errors.append(f"notes/{p.name}: 非法 status '{m.group(1)}'（合法: {'/'.join(sorted(VALID_NOTE_STATUS))}）")
        else:
            note_status = m.group(1)
        for field in ("domain", "module", "created", "review_due"):
            if not re.search(rf"{field}:", fm):
                errors.append(f"notes/{p.name}: frontmatter 缺少字段 {field}")
        for field in ("domain", "module", "created"):
            value = field_value(fm, field)
            if is_placeholder(value):
                errors.append(f"notes/{p.name}: frontmatter 字段 {field} 为空或仍是模板占位符")
        created = re.search(r"^created:\s*(.*?)\s*$", fm, re.M)
        if created and not valid_date(created.group(1).strip('"\'')):
            errors.append(f"notes/{p.name}: created 应为有效日期 YYYY-MM-DD")
        row = roadmap_by_note.get(relative)
        if note_status and row and row["status"] and row["status"] != "⏭️":
            expected = NOTE_TO_ROADMAP.get(note_status)
            if expected and row["status"] != expected:
                errors.append(f"notes/{p.name}: status={note_status} 与 roadmap.md 第{row['line']}行状态不一致")

        due = re.search(r"^review_due:\s*(.*?)\s*$", fm, re.M)
        due_value = due.group(1).strip() if due else None
        if due and due.group(1) not in {"null", "~", '"null"', "'null'"}:
            date_value = due.group(1).strip('"\'')
            if not valid_date(date_value):
                errors.append(f"notes/{p.name}: review_due 应为 YYYY-MM-DD 或 null")
        if note_status == "mastered" and due_value not in {"null", "~", '"null"', "'null'"}:
            errors.append(f"notes/{p.name}: mastered 状态的 review_due 必须为 null")
        for field, allowed in (("review_stage", {"1", "2", "3", "4"}), ("passes_in_stage", {"0", "1"})):
            value = re.search(rf"^{field}:\s*(\d+)\s*$", fm, re.M)
            if value and value.group(1) not in allowed:
                errors.append(f"notes/{p.name}: {field} 值非法: {value.group(1)}")
            elif not value and field == "review_stage" and note_status in {"done", "review"}:
                warns.append(f"notes/{p.name}: 建议补充 {field} 以持久化复习进度")

    for relative in sorted(notes):
        if relative not in linked_notes:
            warns.append(f"{relative}: 没有对应的 roadmap.md 笔记链接")
    for relative, path in notes.items():
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[\[notes/([^]|#]+)", content):
            target = target.strip()
            target = target if Path(target).suffix else f"{target}.md"
            target = f"notes/{target}"
            if target not in notes:
                warns.append(f"{relative}: 双链目标不存在: {target}")


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
    if (root / "research-notes.md").exists():
        check_research_notes(root / "research-notes.md", errors, warns)

    for f in ("profile.md", "roadmap.md"):
        p = root / f
        if p.exists():
            check_schema(p, errors, warns)
    if (root / "profile.md").exists():
        check_profile(root / "profile.md", errors, warns)
    roadmap_rows = check_roadmap(root / "roadmap.md", errors) if (root / "roadmap.md").exists() else []
    check_notes(root, errors, warns, roadmap_rows)

    for w in warns:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERROR] {e}")
    print(f"\n校验结果: {len(errors)} 个错误, {len(warns)} 个警告 → {'FAIL' if errors else 'PASS'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
