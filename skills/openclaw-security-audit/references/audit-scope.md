# Audit Scope

Use this reference when you need the full checklist behind the `openclaw-security-audit` skill.

## Checks

1. Network exposure
- Review `gateway.bind`, `gateway.port`, `gateway.auth.mode`, `gateway.tailscale.mode`, and `gateway.customBindHost`.
- Inspect live listeners on the configured port.
- Treat non-loopback listeners as the most urgent risk.

2. Secret handling
- Check whether gateway tokens, bot tokens, and provider API keys are stored as `${ENV_VAR}` placeholders instead of inline literals.
- Confirm referenced environment variables exist in `.env` when the config expects them.

3. Dangerous local actions
- Review `tools.elevated.enabled`.
- Review dangerous capability groups such as `group:runtime`, `group:web`, `group:ui`, `group:automation`, `group:nodes`, `group:messaging`, `group:memory`, and `image`.
- Note when sandbox mode is off at the same time as risky tools are enabled.

4. Device trust boundary
- Count pending pairings and paired devices.
- Summarize paired device names, roles, and scopes.
- Flag pending requests for human review.

5. Sensitive file protection
- Review ACLs on `.openclaw`, `.openclaw/openclaw.json`, and `.openclaw/.env`.
- Flag inherited or broad allow rules outside the current user, `SYSTEM`, and `Administrators`.

6. Built-in OpenClaw audit
- Run `openclaw security audit --deep --json`.
- Carry built-in findings into the report.
- Treat `gateway.probe_failed` with `ECONNREFUSED` as an availability note unless another check proves public exposure.

7. Leakage prevention
- Ensure `.gitignore` contains `/.openclaw/`, `/AppData/`, and `/openclaw-local.cmd`.
- Ensure `.dockerignore` contains `.openclaw` and `AppData`.

## Safe Autofix Policy

Allowed during unattended runs:

- Create the report directory.
- Add missing ignore-file entries that prevent accidental state or credential leaks.
- Refresh `latest.md` after writing a new timestamped report.

Not allowed without explicit user approval:

- Change bind addresses or authentication settings.
- Rotate or revoke tokens.
- Approve or remove paired devices.
- Change ACL ownership or require Windows admin elevation.
- Enable or disable major tool groups.
- Start exposing new network surfaces.

## Reporting Policy

- Keep the report actionable and plain-language.
- Put automatic fixes in a separate section from manual actions.
- Include exact commands for manual actions when they are known and safe to share.
- Save timestamped reports and refresh `latest.md` on every run.
