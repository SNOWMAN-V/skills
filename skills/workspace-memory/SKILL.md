---
name: workspace-memory
description: Capture, store, and reuse per-workspace work memory. Use when Codex needs to summarize the current day's work into a dated memory file inside the active workspace, read the latest saved memory before continuing work, give a brief progress update from the newest memory, or answer follow-up questions from the detailed notes saved under each topic heading.
---

# Workspace Memory

## Overview

Keep one durable memory stream per workspace. Store memories in a workspace-local `memory/` folder, update the current day's note instead of creating duplicates, and consult the newest memory before resuming work.

## Core Workflow

1. Resolve the workspace root.
- Prefer the Git top-level directory.
- If the directory is not a Git repository, use the current working directory or the workspace root named by the user.

2. Ensure the memory directory exists.
- Use `<workspace-root>/memory/`.
- Keep each workspace isolated. Do not reuse memory files across different workspaces.

3. Read before continuing work.
- Before a new work session, read the newest dated file in `memory/` if one exists.
- Give the user a short progress brief that covers the latest completed work, the current focus, blockers or open risks, and the most likely next step.

4. Write after meaningful work.
- Create or update today's file named `YYYY-MM-DD.md` using the local date.
- Reuse the same file for multiple sessions on the same date instead of creating extra files.

5. Answer from saved memory.
- When the user asks about a topic title, answer from the matching section's detailed notes.
- If the requested topic is not in the newest file, look at older dated files only when the question clearly points to earlier work.
- If the memory does not contain the needed detail, say so plainly and do not invent information.

## Memory File Rules

- Write memory files in Markdown.
- Name each file exactly `YYYY-MM-DD.md`.
- Start each file with a top-level title and workspace marker:
  - `# Memory for YYYY-MM-DD`
  - `Workspace: <absolute-workspace-path>`
- Create one `##` heading per important topic.
- Keep each topic heading short, specific, and easy to scan.
- Under each heading, record the durable details that matter later: decisions, major edits, blockers, commands, test results, file paths, and next steps.
- Prefer concise writing, but include enough detail that a later session can resume without guesswork.
- Skip low-value chatter, obvious command-by-command logs, and temporary thoughts that will not help future work.

## Topic Writing Guidance

For each important topic, capture these points when they exist:

- What changed
- Why it matters
- Current state
- Important files, commands, or outputs
- Next step, blocker, or open question

Use short bullets or compact prose. Choose the format that makes the note easiest to reuse later.

## Progress Brief Rules

- Base the brief on the newest memory file in the current workspace.
- Keep the brief short: usually 2 to 5 sentences or a few compact bullets.
- Mention the last recorded work date.
- Highlight the main completed item, the current focus, and the next step.
- Mention blockers only if they still matter.
- If no memory file exists yet, say that there is no saved memory for this workspace and offer to create today's memory after work.

## Detailed Question Handling

- Match the user's wording to the closest topic heading in memory.
- Answer from the saved notes before using outside context.
- If the user asks for detail under a heading, expand only that section instead of repeating the whole file.
- If several files contain the same topic across different dates, prefer the newest relevant section and mention the date when useful.

## Reference File

Read `references/memory-file-template.md` when you need the canonical structure for a new memory file or a reminder of the short briefing format.

## Example Requests

- "Read the latest memory in this workspace and tell me where we left off."
- "Write today's work into memory."
- "Update today's memory with the testing results and the blocker."
- "What did the 'video prompt optimization' section say in the latest memory?"

