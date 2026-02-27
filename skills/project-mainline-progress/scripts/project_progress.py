#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

BLOCK_PATTERN = re.compile(r"```progress-data\s*(\{.*?\})\s*```", re.DOTALL)


def clamp_progress(value: Any) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"invalid progress value: {value}")
    if number < 0 or number > 100:
        raise ValueError(f"progress must be between 0 and 100 (got {number})")
    return number


def safe_id(raw: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_]", "_", raw.strip())
    text = re.sub(r"_+", "_", text)
    return text or "node"


def esc_label(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    return path.read_text(encoding="utf-8")


def extract_data_from_text(text: str) -> dict[str, Any]:
    match = BLOCK_PATTERN.search(text)
    if not match:
        raise ValueError("progress-data block not found")
    payload = match.group(1)
    try:
        raw_data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in progress-data block: {exc}") from exc
    return normalize_data(raw_data)


def replace_data_block(text: str, data: dict[str, Any]) -> str:
    serialized = json.dumps(data, indent=2, ensure_ascii=False)
    block = f"```progress-data\n{serialized}\n```"
    if BLOCK_PATTERN.search(text):
        return BLOCK_PATTERN.sub(block, text, count=1)
    base = text.rstrip()
    return f"{base}\n\n{block}\n"


def normalize_mainline(mainline: Any) -> list[dict[str, Any]]:
    if not isinstance(mainline, list) or not mainline:
        raise ValueError("mainline must be a non-empty list")

    out: list[dict[str, Any]] = []
    for idx, node in enumerate(mainline, start=1):
        if not isinstance(node, dict):
            raise ValueError(f"mainline node {idx} is not an object")
        node_id = str(node.get("id") or f"M{idx}").strip()
        title = str(node.get("title") or f"Mainline Task {idx}").strip()
        progress = clamp_progress(node.get("progress", 0))
        notes = str(node.get("notes") or "").strip()
        out.append({"id": node_id, "title": title, "progress": progress, "notes": notes})
    return out


def normalize_branches(branches: Any) -> list[dict[str, Any]]:
    if branches is None:
        return []
    if not isinstance(branches, list):
        raise ValueError("branches must be a list")

    out: list[dict[str, Any]] = []
    for b_idx, branch in enumerate(branches, start=1):
        if not isinstance(branch, dict):
            raise ValueError(f"branch {b_idx} is not an object")
        branch_id = str(branch.get("id") or f"B{b_idx}").strip()
        branch_title = str(branch.get("title") or f"Branch {b_idx}").strip()
        from_node = str(branch.get("from") or "").strip()
        items = branch.get("items")
        if items is None:
            items = []
        if not isinstance(items, list):
            raise ValueError(f"branch {branch_id} items must be a list")

        norm_items: list[dict[str, Any]] = []
        for i_idx, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"item {i_idx} in branch {branch_id} is not an object")
            item_id = str(item.get("id") or f"{branch_id}-{i_idx}").strip()
            item_title = str(item.get("title") or f"Branch Task {i_idx}").strip()
            progress = clamp_progress(item.get("progress", 0))
            norm_items.append({"id": item_id, "title": item_title, "progress": progress})

        out.append(
            {
                "id": branch_id,
                "title": branch_title,
                "from": from_node,
                "items": norm_items,
            }
        )
    return out


def normalize_data(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("progress-data must be a JSON object")
    goal = str(raw.get("goal") or "").strip()
    if not goal:
        raise ValueError("goal is required")

    mainline = normalize_mainline(raw.get("mainline"))
    branches = normalize_branches(raw.get("branches"))

    return {
        "goal": goal,
        "mainline": mainline,
        "branches": branches,
    }


def completion_symbol(progress: int) -> str:
    if progress >= 100:
        return "x"
    if progress > 0:
        return "~"
    return " "


def node_state(progress: int) -> str:
    if progress >= 100:
        return "done"
    if progress > 0:
        return "active"
    return "todo"


def connector_for(next_progress: int) -> str:
    if next_progress <= 0:
        return "-----"
    if next_progress < 34:
        return ">----"
    if next_progress < 67:
        return "==>--"
    if next_progress < 100:
        return "====>"
    return "====="


def mainline_progress(mainline: list[dict[str, Any]]) -> float:
    total = sum(node["progress"] for node in mainline)
    return total / len(mainline)


def branch_average(branch: dict[str, Any]) -> float:
    items = branch["items"]
    if not items:
        return 0.0
    return sum(item["progress"] for item in items) / len(items)


def branch_done_count(branch: dict[str, Any]) -> int:
    return sum(1 for item in branch["items"] if item["progress"] >= 100)


def build_text_report(data: dict[str, Any], expand_branches: bool) -> str:
    lines: list[str] = []
    goal = data["goal"]
    mainline = data["mainline"]
    branches = data["branches"]

    total = mainline_progress(mainline)
    done_nodes = sum(1 for node in mainline if node["progress"] >= 100)

    lines.append("Goal")
    lines.append(f"- {goal}")
    lines.append("")
    lines.append("Overall Mainline Progress")
    lines.append(f"- {total:.1f}% ({done_nodes}/{len(mainline)} nodes completed)")
    lines.append("")

    tokens: list[str] = []
    for idx, node in enumerate(mainline):
        symbol = "x" if node["progress"] >= 100 else ("~" if node["progress"] > 0 else " ")
        tokens.append(f"[{node['id']} {symbol} {node['progress']}%]")
        if idx < len(mainline) - 1:
            tokens.append(connector_for(mainline[idx + 1]["progress"]))

    lines.append("Mainline Path")
    lines.append(f"- {' '.join(tokens)}")
    for node in mainline:
        box = completion_symbol(node["progress"])
        lines.append(f"- [{box}] {node['id']} {node['title']} ({node['progress']}%)")
    lines.append("")

    lines.append("Branches")
    if not branches:
        lines.append("- none")
        return "\n".join(lines)

    if not expand_branches:
        for branch in branches:
            avg = branch_average(branch)
            done = branch_done_count(branch)
            total_items = len(branch["items"])
            anchor = branch["from"] or "(no anchor)"
            lines.append(
                f"- {branch['id']} from {anchor}: {branch['title']} ({avg:.1f}%, {done}/{total_items} done)"
            )
        lines.append("- branch details are collapsed (use expand-branches to open)")
        return "\n".join(lines)

    for branch in branches:
        avg = branch_average(branch)
        done = branch_done_count(branch)
        total_items = len(branch["items"])
        anchor = branch["from"] or "(no anchor)"
        lines.append(f"- {branch['id']} from {anchor}: {branch['title']} ({avg:.1f}%, {done}/{total_items} done)")
        if not branch["items"]:
            lines.append("- [ ] no branch tasks yet")
            continue
        for item in branch["items"]:
            box = completion_symbol(item["progress"])
            lines.append(f"- [{box}] {item['id']} {item['title']} ({item['progress']}%)")
    return "\n".join(lines)


def build_mermaid(data: dict[str, Any], expand_branches: bool) -> str:
    mainline = data["mainline"]
    branches = data["branches"]

    lines: list[str] = ["flowchart LR"]
    done_nodes: list[str] = []
    active_nodes: list[str] = []
    todo_nodes: list[str] = []
    branch_nodes: list[str] = []

    id_map: dict[str, str] = {}

    for node in mainline:
        node_id = f"M_{safe_id(node['id'])}"
        id_map[node["id"]] = node_id
        label = esc_label(f"{node['id']} {node['title']}\\n{node['progress']}%")
        lines.append(f'  {node_id}("{label}")')
        state = node_state(node["progress"])
        if state == "done":
            done_nodes.append(node_id)
        elif state == "active":
            active_nodes.append(node_id)
        else:
            todo_nodes.append(node_id)

    for idx in range(len(mainline) - 1):
        left = id_map[mainline[idx]["id"]]
        right = id_map[mainline[idx + 1]["id"]]
        lines.append(f"  {left} --> {right}")

    if expand_branches:
        for branch in branches:
            root_id = f"BR_{safe_id(branch['id'])}"
            anchor = id_map.get(branch.get("from", ""))
            avg = branch_average(branch)
            label = esc_label(f"{branch['id']} {branch['title']}\\n{avg:.0f}%")
            lines.append(f'  {root_id}("{label}")')
            branch_nodes.append(root_id)
            if anchor:
                lines.append(f"  {anchor} --> {root_id}")

            prev = root_id
            for item in branch["items"]:
                item_id = f"BRI_{safe_id(item['id'])}"
                item_label = esc_label(f"{item['id']} {item['title']}\\n{item['progress']}%")
                lines.append(f'  {item_id}("{item_label}")')
                lines.append(f"  {prev} --> {item_id}")
                prev = item_id

                state = node_state(item["progress"])
                if state == "done":
                    done_nodes.append(item_id)
                elif state == "active":
                    active_nodes.append(item_id)
                else:
                    todo_nodes.append(item_id)

    lines.append("  classDef done fill:#9be9a8,stroke:#1a7f37,color:#052e16")
    lines.append("  classDef active fill:#f9d976,stroke:#8b5a00,color:#3d2a00")
    lines.append("  classDef todo fill:#e5e7eb,stroke:#6b7280,color:#111827")
    lines.append("  classDef branch fill:#bfdbfe,stroke:#1d4ed8,color:#0f172a")

    if done_nodes:
        lines.append(f"  class {','.join(done_nodes)} done")
    if active_nodes:
        lines.append(f"  class {','.join(active_nodes)} active")
    if todo_nodes:
        lines.append(f"  class {','.join(todo_nodes)} todo")
    if branch_nodes:
        lines.append(f"  class {','.join(branch_nodes)} branch")

    return "\n".join(lines)


def write_data_back(path: Path, data: dict[str, Any]) -> None:
    text = read_text(path)
    updated = replace_data_block(text, data)
    path.write_text(updated, encoding="utf-8")


def command_init(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if path.exists() and not args.force:
        print(f"error: file exists: {path} (use --force to overwrite)", file=sys.stderr)
        return 1

    if not args.task:
        print("error: at least one --task is required", file=sys.stderr)
        return 1

    mainline = []
    for idx, title in enumerate(args.task, start=1):
        mainline.append(
            {
                "id": f"M{idx}",
                "title": title.strip(),
                "progress": 0,
                "notes": "",
            }
        )

    data = {"goal": args.goal.strip(), "mainline": mainline, "branches": []}

    content = (
        "# Project Progress\n\n"
        "Keep this file focused on progress tracking.\n"
        "Mainline drives overall completion; branches are optional ideas.\n\n"
        "```progress-data\n"
        f"{json.dumps(data, indent=2, ensure_ascii=False)}\n"
        "```\n"
    )

    path.write_text(content, encoding="utf-8")
    print(f"initialized: {path}")
    return 0


def command_set_progress(args: argparse.Namespace) -> int:
    path = Path(args.file)
    text = read_text(path)
    data = extract_data_from_text(text)
    target = args.node.strip()
    progress = clamp_progress(args.progress)

    for node in data["mainline"]:
        if node["id"] == target:
            node["progress"] = progress
            write_data_back(path, data)
            print(f"updated mainline node {target} -> {progress}%")
            return 0

    for branch in data["branches"]:
        for item in branch["items"]:
            if item["id"] == target:
                item["progress"] = progress
                write_data_back(path, data)
                print(f"updated branch node {target} -> {progress}%")
                return 0

    print(f"error: node not found: {target}", file=sys.stderr)
    return 1


def command_add_branch(args: argparse.Namespace) -> int:
    path = Path(args.file)
    text = read_text(path)
    data = extract_data_from_text(text)

    from_id = args.from_node.strip()
    mainline_ids = {node["id"] for node in data["mainline"]}
    if from_id not in mainline_ids:
        print(f"error: from node '{from_id}' is not in mainline", file=sys.stderr)
        return 1

    branch_id = args.branch_id.strip()
    if any(branch["id"] == branch_id for branch in data["branches"]):
        print(f"error: branch id already exists: {branch_id}", file=sys.stderr)
        return 1

    items: list[dict[str, Any]] = []
    for idx, title in enumerate(args.task or [], start=1):
        items.append({"id": f"{branch_id}-{idx}", "title": title.strip(), "progress": 0})

    data["branches"].append(
        {
            "id": branch_id,
            "title": args.title.strip(),
            "from": from_id,
            "items": items,
        }
    )

    write_data_back(path, data)
    print(f"added branch {branch_id} from {from_id}")
    return 0


def command_report(args: argparse.Namespace) -> int:
    text = read_text(Path(args.file))
    data = extract_data_from_text(text)

    out_parts: list[str] = []
    if args.format in ("text", "both"):
        out_parts.append(build_text_report(data, args.expand_branches))
    if args.format in ("mermaid", "both"):
        out_parts.append("Mermaid\n```mermaid\n" + build_mermaid(data, args.expand_branches) + "\n```")

    print("\n\n".join(out_parts))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mainline-first project progress utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a new PROJECT_PROGRESS.md")
    init_parser.add_argument("--file", required=True, help="target markdown file")
    init_parser.add_argument("--goal", required=True, help="final project goal")
    init_parser.add_argument("--task", action="append", help="mainline task title", default=[])
    init_parser.add_argument("--force", action="store_true", help="overwrite existing file")
    init_parser.set_defaults(func=command_init)

    set_parser = subparsers.add_parser("set-progress", help="set progress for a node id")
    set_parser.add_argument("--file", required=True, help="target markdown file")
    set_parser.add_argument("--node", required=True, help="node id such as M2 or B1-1")
    set_parser.add_argument("--progress", required=True, type=int, help="progress 0-100")
    set_parser.set_defaults(func=command_set_progress)

    branch_parser = subparsers.add_parser("add-branch", help="add an optional branch")
    branch_parser.add_argument("--file", required=True, help="target markdown file")
    branch_parser.add_argument("--from", dest="from_node", required=True, help="mainline node id")
    branch_parser.add_argument("--branch-id", required=True, help="branch id, for example B1")
    branch_parser.add_argument("--title", required=True, help="branch title")
    branch_parser.add_argument("--task", action="append", default=[], help="branch task title")
    branch_parser.set_defaults(func=command_add_branch)

    report_parser = subparsers.add_parser("report", help="render progress report")
    report_parser.add_argument("--file", required=True, help="target markdown file")
    report_parser.add_argument("--format", choices=["text", "mermaid", "both"], default="both")
    report_parser.add_argument("--expand-branches", action="store_true")
    report_parser.set_defaults(func=command_report)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

