# Handoff Template

Use this template when creating or refreshing `<project-root>/.codex-handoff.md`.

## Template

````md
# Handoff

## Goal
State the concrete project goal and the desired finished result.

## Current Status
Completed:
- ...

In progress:
- ...

Not started:
- ...

## Files Touched
- /absolute/path/to/file - why it matters

## Decisions
- Chosen approach and why
- Rejected approach if it matters

## Constraints
- Things that must not change
- Compatibility or environment requirements
- Scope limits the next session should respect

## Next Steps
1. First concrete action
2. Second concrete action
3. Verification or follow-up action

## Verify
```powershell
# Real commands only
```

## Risks / Open Questions
- Unknowns, blockers, or places that need extra care

## Resume Prompt
Please read `<project-root>/.codex-handoff.md`, continue with the Next Steps, and update the handoff file after meaningful progress.
````

## Notes

- Prefer concise, high-signal bullets over long prose.
- Use absolute file paths when they help the next session move faster.
- Skip sections that are truly irrelevant, but keep `Goal`, `Current Status`, `Next Steps`, and `Resume Prompt`.
- Do not copy full chat transcripts into the handoff.
- Do not include chat IDs, session IDs, tokens, or secrets unless the user explicitly asks for them.

## Ready-To-Send Resume Prompt

When the user asks for "做好交接准备工作", return a prompt they can send from Telegram or a fresh session. Adapt the path to the real project root.

```text
/new <project-root>
请先阅读 <project-root>/.codex-handoff.md，然后继续执行 Next Steps；完成有意义的进展后，更新这个交接文件并汇报结果。
```