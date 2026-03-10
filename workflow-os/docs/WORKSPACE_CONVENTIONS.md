# Workspace Conventions

## Purpose

Workflow OS uses `D:\skills\workflow-os` as the single control workspace for routing work, storing durable rules, and centralizing artifacts.

## Directory Roles

- `apps/`: local apps and UI surfaces, including future mission-control work.
- `config/`: committed non-secret configuration and policy files.
- `data/`: database files, schema files, and other structured local data.
- `docs/`: durable specifications, policies, and frozen decisions.
- `imports/opensource/`: imported open-source projects that are evaluated or adapted locally.
- `memory/`: workspace-local memory notes written by date.
- `outputs/reports/`: shared reports that are not owned by a specific skill.
- `outputs/skills/`: managed skill-owned artifacts.
- `registry/`: machine-readable catalogs for skills, tools, and later adapters.
- `runtime/`: transient runtime state, caches, and supervisor scratch files.
- `scripts/`: local admin and bootstrap scripts for Workflow OS itself.

## Managed Output Rules

### Default Rule

Every skill that writes durable artifacts should write into:

`D:\skills\workflow-os\outputs\skills\<skill-slug>\`

### Default Subfolders

When useful, use these standard subfolders under each skill root:

- `research/`
- `reports/`
- `plans/`
- `locks/`
- `snapshots/`
- `artifacts/`
- `logs/`

### Special Cases

- `workspace-memory` writes to `D:\skills\workflow-os\memory\`
- `project-handoff` may still write `.codex-handoff.md` in the target project root, but Workflow OS may mirror copies or indexes under `outputs/skills/project-handoff/`
- `project-mainline-progress` may still keep `PROJECT_PROGRESS.md` in the target project root, with optional centralized snapshots under `outputs/skills/project-mainline-progress/`

## Skill Governance Rules

- Use the folder name as the current stable skill ID until a normalization pass is complete.
- Track every skill in `registry/skills-registry.json`.
- Record both the physical skill path and the managed output path.
- Flag naming inconsistencies and missing metadata instead of silently ignoring them.
- Avoid writing reports and generated files back into the skill source folders unless the skill is explicitly source-owned.

## Import Rules for Open-Source Projects

- Store imported third-party projects under `imports/opensource/`.
- Keep each imported project in its own subfolder.
- Record source URL, license, local path, and evaluation status in the database once repository tracking is added.
- Do not commit third-party repos blindly; inspect license, secrets, and unnecessary history first.

## SQLite vs Markdown Split

Use SQLite for:

- tasks
- runs
- skill records
- tool records
- artifacts
- decisions
- imported repository inventory
- searchable memory metadata

Use Markdown for:

- frozen goal locks
- long-form reasoning or design docs
- handoff files
- daily human-readable memory notes
- security policies and checklists

## Local-Only by Default

These paths should remain local-only unless explicitly reviewed and approved:

- `data/*.db*`
- `runtime/**`
- `outputs/**`
- `memory/**`
- `imports/opensource/**`
- any `.env*`, `*.pem`, `*.key`, or secret-bearing local config file

## Naming Guidance

- Prefer lowercase hyphen-case for new skill folders.
- Use lowercase snake_case or kebab-case consistently for machine-readable file names.
- Use descriptive top-level document names for project policies and architecture records.

## Review Gate

Before pushing to GitHub, run the local pre-push safety check and manually confirm that no secret, token, personal note, or third-party repo dump is being synced.
