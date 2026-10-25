#!/usr/bin/env python3
"""校验 Skill 的岗位/领域/行业路由、静态案例引用、模块结构和知识骨架掌握证据。

用法: validate_skill.py [项目根目录，默认当前目录]
退出码: 0=结构通过（允许内容警告），1=有结构错误
"""
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "① 领域画像",
    "② 细分路由",
    "③ 预设知识骨架",
    "④ 权威信源清单",
    "⑤ 进阶检查点",
    "⑥ 常见误区",
)
EVIDENCE_HINTS = re.compile(r"(?:^|[；，：。—(（])\s*(?:能(?:够)?|可以|可独立|可用|会)(?:[，：；、\s]|[\u4e00-\u9fff])")
TREE_BRANCH = re.compile(r"^((?:(?:│   )|(?:    ))*)(?:├──|└──)\s*(.+)$")


def split_cells(line: str) -> list:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def check_module(path: Path, errors: list, warns: list) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    for heading in REQUIRED_SECTIONS:
        matches = [i for i, line in enumerate(lines) if line.strip() == f"## {heading}"]
        if not matches:
            errors.append(f"{path}: 缺少章节标题 '## {heading}'")
            continue
        if len(matches) > 1:
            errors.append(f"{path}: 章节标题重复 '## {heading}'")

    start = next((i for i, line in enumerate(lines) if line.strip() == "## ③ 预设知识骨架"), None)
    end = next((i for i, line in enumerate(lines[start + 1:], start + 1) if line.startswith("## ")), len(lines)) if start is not None else len(lines)
    section = lines[start:end] if start is not None else []
    fences = [i for i, line in enumerate(section) if line.strip().startswith("```")]
    tree_lines = []
    if len(fences) >= 2:
        first_tree_line = start + fences[0] + 2
        for offset, line in enumerate(section[fences[0] + 1:fences[1]]):
            match = TREE_BRANCH.match(line)
            if match:
                depth = len(match.group(1)) // 4
                if depth >= 6:
                    errors.append(f"{path}:{first_tree_line + offset}: 知识骨架超过 6 层")
                tree_lines.append((first_tree_line + offset, depth, match.group(2).strip()))
            elif "├──" in line or "└──" in line:
                errors.append(f"{path}:{first_tree_line + offset}: 树节点缩进格式无法识别")
    if not tree_lines:
        errors.append(f"{path}: ③ 预设知识骨架中未找到可识别的树状节点")
        return

    leaves = 0
    for index, (line_number, depth, content) in enumerate(tree_lines):
        has_children = False
        for _, later_depth, _ in tree_lines[index + 1:]:
            if later_depth <= depth:
                break
            has_children = True
            break
        if has_children:
            continue
        leaves += 1
        if not EVIDENCE_HINTS.search(content):
            warns.append(f"{path}:{line_number}: 叶子节点缺少明确的能力证据（建议用“能/可以/会”写出可观察的表现）：{content}")
    if not leaves:
        errors.append(f"{path}: 知识骨架没有可识别的叶子节点")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(".")
    if len(sys.argv) > 2:
        sys.exit("用法: validate_skill.py [项目根目录]")
    if not root.is_dir():
        sys.exit(f"目录不存在: {root}")

    errors, warns = [], []
    skill_file = root / "SKILL.md"
    domains_root = root / "references/domains"
    role_routes_file = root / "references/core/role-routing.md"
    industries_root = root / "references/industries"
    industry_index = industries_root / "_index.md"
    routing_evals = root / "docs/evals/role-routing.md"
    if not skill_file.is_file():
        errors.append("缺少 SKILL.md")
    if not domains_root.is_dir():
        errors.append("缺少 references/domains/")
    if not role_routes_file.is_file():
        errors.append("缺少 references/core/role-routing.md")
    if not industry_index.is_file():
        errors.append("缺少 references/industries/_index.md")
    if not routing_evals.is_file():
        errors.append("缺少 docs/evals/role-routing.md")
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    skill_text = skill_file.read_text(encoding="utf-8")
    l1_routes = re.findall(r"`(references/domains/[^`]+/_index\.md)`", skill_text)
    if not l1_routes:
        errors.append("SKILL.md: 未找到 L1 领域路由目标")
    for route in l1_routes:
        if not (root / route).is_file():
            errors.append(f"SKILL.md: L1 路由目标不存在: {route}")

    routing_docs = [role_routes_file, industry_index, routing_evals]
    routing_docs.extend(path for path in industries_root.glob("*.md") if path.name != "_index.md")
    for doc in routing_docs:
        text = doc.read_text(encoding="utf-8")
        for route in re.findall(r"`((?:references/(?:domains|industries)/)[^`]+\.md)`", text):
            if not (root / route).is_file():
                errors.append(f"{doc}: 路由目标不存在: {route}")

    for route in re.findall(r"`([^`/]+\.md)`", industry_index.read_text(encoding="utf-8")):
        if not (industries_root / route).is_file():
            errors.append(f"{industry_index}: 行业叠加目标不存在: {route}")
    eval_text = routing_evals.read_text(encoding="utf-8")
    case_definitions = eval_text.split("## 走查结果记录", 1)[0]
    case_ids = re.findall(r"^\| (RR-\d+) \|", case_definitions, re.M)
    if len(case_ids) < 5:
        errors.append(f"{routing_evals}: 静态路由案例少于 5 个")
    if len(case_ids) != len(set(case_ids)):
        errors.append(f"{routing_evals}: 静态路由案例 ID 重复")

    indexes = sorted(domains_root.glob("*/_index.md"))
    for index in indexes:
        if index.relative_to(root).as_posix() not in l1_routes:
            warns.append(f"{index}: 未在 SKILL.md 的 L1 路由表中引用")
        routed_files = set()
        for line_number, line in enumerate(index.read_text(encoding="utf-8").splitlines(), 1):
            if "|" not in line:
                continue
            cells = split_cells(line)
            if len(cells) < 3:
                continue
            file_match = re.fullmatch(r"`([^`]+\.md)`", cells[2])
            if not file_match:
                continue
            module_name = file_match.group(1)
            module_path = index.parent / module_name
            if not module_path.is_file():
                errors.append(f"{index}:{line_number}: L2 路由目标不存在: {module_name}")
                continue
            if module_name in routed_files:
                errors.append(f"{index}:{line_number}: L2 路由目标重复: {module_name}")
            routed_files.add(module_name)
            check_module(module_path, errors, warns)

        for module_path in sorted(index.parent.glob("*.md")):
            if module_path.name != "_index.md" and module_path.name not in routed_files:
                warns.append(f"{module_path}: 模块文件未在 _index.md 中注册")

    for warning in warns:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}")
    print(f"\n校验结果: {len(errors)} 个结构错误, {len(warns)} 个内容警告 → {'FAIL' if errors else 'PASS'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
