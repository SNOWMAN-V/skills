# GitHub Safety Policy

## Goal

Protect Workflow OS from leaking secrets, private notes, sensitive runtime state, or unreviewed third-party content during GitHub sync.

## Never Push Without Review

Always review these categories before pushing:

- API keys, tokens, passwords, cookies, or private credentials
- `.env` files or local-only config files
- SQLite databases and runtime state
- daily memory notes that may contain private context
- imported third-party repositories under `imports/opensource/`
- generated outputs under `outputs/`
- security reports that expose local machine details

## Local-Only Paths

Treat these as local-only by default:

- `memory/`
- `outputs/`
- `runtime/`
- `imports/opensource/`
- `data/*.db*`
- `config/local.*`

## Required Pre-Push Flow

1. Run:
   `powershell -ExecutionPolicy Bypass -File .\workflow-os\scripts\pre_push_check.ps1`
2. Review `git status --short`
3. Review `git diff --staged` and `git diff --cached --name-only`
4. Confirm no local-only files are staged
5. Confirm no imported third-party repo is being pushed without license review
6. Confirm no report exposes device-specific secrets, auth state, or paired-device details

## High-Risk Patterns

The pre-push check should be treated as blocking when it finds:

- private key blocks
- `api_key`, `token`, `secret`, `password` assignments
- OpenAI-style `sk-` keys
- AWS access key patterns
- `.pem`, `.key`, `.p12`, `.env` files in tracked content

## Human Approval Rule

If a push includes new automation, new remote execution capability, or new imported open-source code, do one extra manual review pass before pushing.

## Default Policy

If a file might be sensitive and you are not sure, keep it local until it is explicitly reviewed.
