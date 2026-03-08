---
name: project-handoff
description: Prepare, refresh, or read a reusable project handoff file so work can move cleanly between Codex desktop, Telegram, or later sessions without losing context. Use when the user says 做交接, 更新交接, 做好交接准备工作, 读取交接, handoff, 接着上次继续, or asks to prepare current work before leaving the computer.
---

# Project Handoff

Use this skill to turn the current state of work into a durable handoff that another Codex session can resume quickly.

Read [references/handoff-template.md](references/handoff-template.md) only when you need the exact template sections or the ready-to-send resume prompt.

## Default Behavior

- Treat `请你做好交接准备工作` as a command to prepare a full handoff now.
- Prefer the git repo root from `git rev-parse --show-toplevel` for the handoff location. If the directory is not a git repo, use the current working directory.
- Default handoff file path to `<project-root>/.codex-handoff.md`.
- Update the existing handoff file in place if it already exists. Preserve useful manual notes, but rewrite stale status so the file reflects the latest project state.
- Do not record Telegram chat IDs, desktop conversation IDs, bot tokens, API keys, or other secrets unless the user explicitly asks for them.
- When information is missing but the risk is low, make a reasonable assumption and write that assumption into the handoff instead of blocking on questions.

## Workflow

### 1. Gather the latest project state

Inspect only the context needed to create a trustworthy handoff:

- Read the existing handoff file first if it exists.
- Check the project root and active workspace.
- If this is a git repo, inspect `git status --short` and recent diffs for the files relevant to the current task.
- Read the specific files, notes, or test outputs that determine current progress.
- Include user decisions already made in the conversation when they matter for the next session.

### 2. Write or refresh the handoff file

Create or update `<project-root>/.codex-handoff.md` using the template in [references/handoff-template.md](references/handoff-template.md).

Make the file immediately actionable:

- Fill in the concrete goal, not a vague summary.
- Separate what is finished, in progress, and not started.
- List touched files with short reasons when you know them.
- State decisions, constraints, and known risks.
- Write the next steps so another Codex instance can start working without asking what to do next.
- Add verification commands only when they are real and useful.
- Include a short resume prompt that the user can send from Telegram or a fresh desktop session.

### 3. Tailor behavior to the request

If the user asks to "做好交接准备工作":

- Create or refresh the handoff file.
- Return the handoff file path.
- Return a ready-to-send resume prompt that points the next session at the handoff file.

If the user asks to "做交接" or "更新交接":

- Refresh the handoff file with the newest state.
- Briefly summarize what changed in the handoff.

If the user asks to "读取交接" or "接着上次继续":

- Read the handoff file first.
- Summarize the current state back to the user.
- Continue from the `Next Steps` section unless the user redirects you.
- After meaningful progress, update the handoff again before finishing.

## Quality Bar

A good handoff should let a new Codex session answer these questions within seconds:

- What are we trying to accomplish?
- What has already been done?
- What files matter most?
- What should happen next?
- How do we verify success?

If the handoff does not answer those questions clearly, improve it before stopping.