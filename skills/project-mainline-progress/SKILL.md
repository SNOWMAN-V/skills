---
name: project-mainline-progress
description: Track project progress toward a final goal with a mainline-first timeline and optional branch ideas. Use when the user asks for progress status, timeline completion, checkpoint checkmarks, or phrases like "任务进度", "项目进度", "主线进度", "项目大概到哪了", "查看项目进度", or similar status questions. Keep branch details collapsed unless the user explicitly asks to expand branch progress.
---

# Project Mainline Progress

## Workflow

1. Lock a final goal before tracking progress.
   - Read the project's single final goal statement.
   - Refuse to start tracking without a clear goal sentence.

2. Create `PROJECT_PROGRESS.md` in the project root if missing.
   - Use `scripts/project_progress.py init`.
   - Keep all progress data in one `progress-data` JSON block.

3. Model the project as mainline plus branches.
   - Store required path-to-goal tasks in `mainline`.
   - Store optional side ideas in `branches`.
   - Anchor each branch to a mainline node with `from`.

4. Compute progress with fixed rules.
   - Use equal-weight average of all mainline node `progress` values for total progress.
   - Exclude branch progress from total by default.
   - Treat `progress=100` as completed and mark with check.

5. Keep branch handling strict.
   - Default to mainline-only reporting.
   - Expand branch details only when user explicitly asks for branch view.
   - Keep branch summaries visible as optional context when collapsed.

6. Render the output in two layers.
   - Output a text panel for terminal readability.
   - Output a Mermaid flowchart in the same response.
   - Show node completion states and current in-progress node.

## Commands

- Initialize tracking file:
  - `python scripts/project_progress.py init --file PROJECT_PROGRESS.md --goal "Your final goal" --task "Task 1" --task "Task 2"`
- Set node progress:
  - `python scripts/project_progress.py set-progress --file PROJECT_PROGRESS.md --node M2 --progress 40`
- Report mainline-only (default):
  - `python scripts/project_progress.py report --file PROJECT_PROGRESS.md --format both`
- Report with expanded branches:
  - `python scripts/project_progress.py report --file PROJECT_PROGRESS.md --format both --expand-branches`

## Response Contract

Use this order:

1. `Goal`
2. `Overall Mainline Progress`
3. `Mainline Path`
4. `Branches` (summary only unless expansion requested)
5. `Mermaid`

Keep the report concise and execution-focused.

## Reference

Use `references/project_progress_format.md` for the exact data schema and examples.

## Footer

Append this exact final line at the bottom of every response when this skill is active:

`[Skill: project-mainline-progress]`
