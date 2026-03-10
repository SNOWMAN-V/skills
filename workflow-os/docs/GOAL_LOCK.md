# Goal Lock

- Lock ID: `WOS-2026-03-11-01`
- Revision: `1`
- Freeze Date: `2026-03-11`
- Time Zone: `Asia/Shanghai`
- Workspace: `D:\skills\workflow-os`

## Core Objective

Build a local-first workflow operating system inside this repository so software and non-software work can be routed through multi-agent collaboration, reuse existing tools and skills, centralize outputs and data, and keep human review and security checks in the loop.

## Core Features

1. Unified request-to-delivery workflow for many kinds of work.
2. Multi-agent role split with router, executor, reviewer, and human checkpoints.
3. Central workspace with fixed locations for apps, data, imports, outputs, memory, and runtime state.
4. Managed skill library with a registry and standardized output destinations.
5. Local SQLite data layer with strong search and memory support.
6. Visual mission-control surface for progress, runs, and artifacts.
7. Security checks before any GitHub push.

## Hard Constraints

### must

- Keep the project under `D:\skills`.
- Reuse the current skills and existing local tools as much as practical.
- Store skill-generated files inside managed workspace output paths.
- Use SQLite as the first database choice.
- Keep OpenClaw-compatible remote execution in scope.
- Add secret and sensitive-file checks before GitHub pushes.

### must not

- Scatter outputs across arbitrary folders.
- Design the system for coding work only.
- Commit secrets, tokens, API keys, or sensitive personal notes.
- Depend on one external platform as the only control plane.

## Non-Goals for V1

- Finish every downstream automation on day one.
- Fully build stock-trading and video-production systems in the first milestone.
- Replace Codex, OpenClaw, Antigravity, or OpenCode themselves.
- Polish the final dashboard before the workspace conventions and data model exist.

## Acceptance Criteria

- A workspace root exists with a stable directory layout.
- A skill registry exists and defines managed output paths.
- A SQLite database exists with an initial schema for tasks, runs, skills, tools, artifacts, and decisions.
- One sample project can move through idea, scouting, goal lock, execution tracking, and artifact storage.
- A first mission-control UI scaffold exists.
- GitHub safety rules exist before the next push.

## Priority Order

- `P0`: workspace layout, registry, output conventions, SQLite, and security rules
- `P1`: orchestration layer and first end-to-end demo flow
- `P2`: visual dashboard and more domain adapters

## Boundary Guardrails

### In Bound

- Workspace design
- Skill cleanup
- Output path conventions
- SQLite schema
- Multi-agent orchestration
- Dashboard scaffold
- Security push checks

### Out of Bound

- Shipping every domain workflow before the core platform exists
- Treating external tools as replaceable in the first milestone
- Syncing sensitive local data to GitHub
