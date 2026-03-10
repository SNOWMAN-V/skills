# Workflow OS: Task List and Idea Notes

## Workspace and Conventions

- [x] Create the workspace root at `D:\skills\workflow-os`.
- [x] Create the first-pass directory layout for apps, data, imports, outputs, memory, registry, config, docs, and runtime.
- [ ] Define the canonical output path rules for every skill.
- [ ] Decide how imported open-source projects should be stored under `imports/opensource/`.
- [ ] Define which files belong in the repo and which files must stay local-only.
- [ ] Add GitHub push safety checks for secrets, tokens, and sensitive notes.

## Skills Integration

- [ ] Inventory all skills in `D:\skills\skills`.
- [ ] Build a skill registry that records each skill's purpose, inputs, outputs, and owner path.
- [ ] Normalize skills with inconsistent naming or missing metadata.
- [ ] Identify which skills create files and assign each one a managed output directory.
- [ ] Decide how the `central_router` skill should dispatch other skills in the future workflow.

## SQLite and Memory System

- [ ] Create the first local SQLite database for Workflow OS.
- [ ] Design the initial schema for tasks, runs, tools, skills, artifacts, decisions, and memory records.
- [ ] Enable a full-text search strategy based on SQLite FTS5.
- [ ] Define the fallback search flow: precise search first, broader extraction and model analysis second.
- [ ] Decide what should live in SQLite versus what should stay as Markdown files.

## Multi-Agent Architecture

- [ ] Define the first role map for router, executor, reviewer, and human approval.
- [ ] Decide how Codex, OpenCode, Antigravity, and OpenClaw fit into the control plane.
- [ ] Design the run lifecycle from request intake to artifact delivery.
- [ ] Define where intermediate review checkpoints happen.
- [ ] Decide how failures, retries, and supervisor interventions are recorded.

## Visual Mission Control

- [ ] Define the first version of the dashboard scope.
- [ ] Decide whether the first visual surface should be a local web app, a browser page, or a lightweight desktop wrapper.
- [ ] Show project progress, current run status, output artifacts, and alerts in one place.
- [ ] Add a place to inspect database-backed history and skill execution records.

## Open-Source Foundations to Evaluate

- [ ] Evaluate LangGraph as the orchestration core.
- [ ] Evaluate CrewAI as a role-based multi-agent pattern reference.
- [ ] Evaluate Flowise as a visual workflow reference.
- [ ] Evaluate n8n as an integration sidecar, not the main brain.
- [ ] Evaluate Dify as a product reference, not a drop-in replacement.

## Safety and GitHub Hygiene

- [ ] Create a local-only secrets policy for this workspace.
- [ ] Add a pre-push review checklist.
- [ ] Decide which directories should never be synced to GitHub.
- [ ] Audit imported open-source projects before committing anything derived from them.
- [ ] Review OpenClaw and related remote execution surfaces before exposing new automation paths.

## First Delivery Milestone

- [ ] Finalize the workspace conventions.
- [ ] Create the skill registry.
- [ ] Create the SQLite database and first schema.
- [ ] Build one sample end-to-end workflow.
- [ ] Persist outputs into managed directories.
- [ ] Record the run and surface it in a basic mission-control view.

## Notes

- The system should serve much more than coding work.
- The main value is integration, consistency, traceability, and safety.
- The workspace should become the single place where tools, imports, outputs, memory, and rules meet.
