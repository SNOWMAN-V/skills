# PROJECT_PROGRESS.md Format

Use one file per project root: `PROJECT_PROGRESS.md`.

## Data Block

Store machine-readable data inside one fenced block:

```markdown
```progress-data
{
  "goal": "Ship MVP to first 100 users",
  "mainline": [
    { "id": "M1", "title": "Define scope", "progress": 100, "notes": "" },
    { "id": "M2", "title": "Build core flow", "progress": 45, "notes": "" },
    { "id": "M3", "title": "Release", "progress": 0, "notes": "" }
  ],
  "branches": [
    {
      "id": "B1",
      "title": "Experiment onboarding variant",
      "from": "M2",
      "items": [
        { "id": "B1-1", "title": "Prototype A", "progress": 20 },
        { "id": "B1-2", "title": "User test", "progress": 0 }
      ]
    }
  ]
}
```
```

## Rules

- Keep `goal` as one clear final-goal sentence.
- Treat `mainline` as the required path to completion.
- Treat `branches` as optional ideas and experiments.
- Keep `progress` in `[0, 100]`.
- Use equal-weight average of `mainline.progress` for overall project completion.
- Exclude branch progress from overall completion unless explicitly requested.

## CLI Quick Start

- Initialize file:
  - `python scripts/project_progress.py init --file PROJECT_PROGRESS.md --goal "..." --task "..." --task "..."`
- Update node:
  - `python scripts/project_progress.py set-progress --file PROJECT_PROGRESS.md --node M2 --progress 60`
- Add branch:
  - `python scripts/project_progress.py add-branch --file PROJECT_PROGRESS.md --from M2 --branch-id B1 --title "Idea" --task "Task A"`
- Render report:
  - `python scripts/project_progress.py report --file PROJECT_PROGRESS.md --format both`
- Expand branches:
  - `python scripts/project_progress.py report --file PROJECT_PROGRESS.md --format both --expand-branches`
