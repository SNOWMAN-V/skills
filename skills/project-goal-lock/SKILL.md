---
name: project-goal-lock
description: Lock a project's core objective, core features, hard constraints, and acceptance criteria before execution, then enforce objective alignment throughout delivery to prevent requirement drift or forgotten priorities. Use when the user asks to define project purpose, clarify core requirements, keep implementation strictly on target, or recover work that has drifted away from the intended goal.
---

# Project Goal Lock

## Workflow

1. Create a Goal Lock Record before implementation.
   - Capture a single-sentence core objective.
   - Capture 3-7 core features.
   - Capture hard constraints as `must` and `must not` rules.
   - Capture explicit non-goals.
   - Capture testable acceptance criteria.
   - Capture priority order with `P0`, `P1`, `P2`.
   - Capture boundary guardrails with in-bound and out-of-bound examples.
   - Ask only missing critical questions needed to complete the record.

2. Freeze the target with explicit confirmation.
   - Show the complete Goal Lock Record back to the user.
   - Request explicit confirmation to freeze it.
   - Treat the record as immutable after confirmation.
   - If confirmation is missing or rejected, continue clarification only and do not execute implementation work.
   - Refuse silent scope expansion.

3. Build and preserve a Goal Memory Capsule after freeze.
   - Create a stable capsule with lock ID, freeze timestamp, revision, objective, features, constraints, non-goals, and acceptance criteria.
   - Reuse the exact frozen wording for these fields in later outputs.
   - Treat the capsule as the source of truth for all alignment checks.
   - Update capsule contents only through approved `Change Delta`.

4. Run a pre-action alignment check before substantial work.
   - Validate that the next action directly supports at least one core feature.
   - Validate that the action does not violate any hard constraint.
   - Validate that the action does not enter any non-goal.
   - Mark boundary status as `aligned` or `not aligned`.
   - Stop and propose an aligned alternative if any check fails.

5. Perform drift detection at each milestone.
   - Output an `Alignment Snapshot`.
   - Run a memory recall check against the Goal Memory Capsule and mark `consistent` or `inconsistent`.
   - Map completed work to core features.
   - List unresolved gaps against acceptance criteria.
   - Flag drift risks and propose correction steps.
   - If recall is inconsistent, restate the frozen wording and correct before continuing.

6. Apply strict change control when scope changes.
   - Produce a `Change Delta` with:
     - Requested change
     - Unchanged locked items
     - Impact on complexity, timeline, and testing
     - Approval status
   - Update the Goal Lock Record and Goal Memory Capsule only after explicit user approval.
   - Keep previous frozen revision if approval is denied.

7. Close with acceptance proof.
   - Produce an `Acceptance Check` that maps every acceptance criterion to evidence.
   - Mark each criterion as `pass`, `partial`, or `fail`.
   - Provide a final boundary verdict as `aligned` or `not aligned`.

## Response Format

Use these headings exactly:
- `Goal Lock Record`
- `Freeze Confirmation`
- `Alignment Snapshot`
- `Change Delta` (only when scope changes)
- `Acceptance Check`

## Reference

Use [goal-lock-template.md](references/goal-lock-template.md) as the default structure.

## Operating Rules

- Preserve objective fidelity over adding extra features.
- State "not aligned" immediately when a request conflicts with locked constraints.
- Block out-of-bound requests unless the user explicitly approves a `Change Delta`.
- Reuse stable wording for goals, features, and constraints to reduce ambiguity.
- Re-anchor to the Goal Memory Capsule whenever the conversation drifts or becomes ambiguous.
- Ask for clarification early instead of guessing on core requirements.
