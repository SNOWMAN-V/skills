---
name: openclaw-security-audit
description: Comprehensive OpenClaw security review and low-risk hardening for local deployments. Use when Codex needs to inspect OpenClaw for public exposure, unsafe bind/auth settings, paired-device risk, dangerous tool permissions, ACL drift, sensitive files, built-in security audit findings, or recurring daily security reports.
---

# OpenClaw Security Audit

Use this skill to audit a local OpenClaw install, apply only safe low-risk fixes, and produce a durable Markdown report for the user.

Read [references/audit-scope.md](references/audit-scope.md) for the full checklist and fix boundaries. Read [references/report-template.md](references/report-template.md) when you need the exact report sections.

## Default Behavior

- Default OpenClaw root to `D:/Openclaw/openclaw`.
- Default report directory to `D:/skills/skills/openclaw-security-audit/reports` when that path exists. Otherwise use the skill-local `reports/` folder.
- For recurring runs, update both a timestamped report and `latest.md`.
- Apply only safe low-risk fixes during unattended automation.
- Treat high-impact config changes as manual remediation unless the user explicitly approves them.
- Answer these two questions first: `Is it publicly exposed?` and `Can it perform dangerous local actions?`

## Workflow

### 1. Resolve paths

- Confirm `OpenClawRoot`, `StateDir`, `ConfigPath`, and `ReportDir`.
- Prefer the user's runtime wrapper if one exists. Otherwise use `.openclaw` under the repo root.
- Create the report directory if it does not exist.

### 2. Gather evidence

Inspect only the paths and commands needed to support a trustworthy report.

- Read `.openclaw/openclaw.json` and `.openclaw/.env`.
- Inspect paired and pending device metadata under `.openclaw/devices/`.
- Inspect ACLs on `.openclaw`, `.openclaw/openclaw.json`, and `.openclaw/.env`.
- Inspect the live listener for the configured gateway port with `Get-NetTCPConnection` or `netstat`.
- Run the built-in OpenClaw audit with `node dist/index.js security audit --deep --json`.
- Review `.gitignore` and `.dockerignore` for local-state leakage.
- If needed, read [CHANGELOG.md](D:/Openclaw/openclaw/CHANGELOG.md) for recent security hardening context.

### 3. Apply safe low-risk fixes

Allowed during manual or automated runs:

- Create the report directory.
- Add missing ignore-file entries that prevent accidental state leakage.
- Refresh `latest.md` after writing the new timestamped report.

Do not do these without explicit user approval:

- Change bind/auth/tailscale settings.
- Rotate or revoke tokens.
- Approve or remove paired devices.
- Rework ACL ownership or anything that needs Windows admin elevation.
- Expand dangerous tool groups or enable elevated mode.

### 4. Write the report

- Save the report to `D:/skills/skills/openclaw-security-audit/reports`.
- Use the template in [references/report-template.md](references/report-template.md).
- Separate `Automatic Fixes Applied` from `Manual Actions`.
- When there are manual steps, include exact commands when you know them safely.

### 5. Handle recurring checks

- For daily automation, keep the run non-destructive beyond the safe low-risk fixes above.
- Always write a fresh timestamped report and refresh `latest.md`.
- Summarize the highest-risk finding in plain Chinese when reporting back to the user.

## Output Expectations

- Produce a Markdown report with severity counts, plain-language conclusions, findings, automatic fixes, manual actions, and verification commands.
- Keep the report readable enough for a weekly human review.
- When replying in chat, link the saved report path and summarize only the top risks.
