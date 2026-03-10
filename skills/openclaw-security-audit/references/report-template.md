# Report Template

Use this structure for every report written by `openclaw-security-audit`.

## Header

- Generated time
- OpenClaw root
- State dir
- Config path
- Report dir
- OpenClaw version when available

## Executive Summary

Include these six lines near the top:

- Overall status: `green`, `yellow`, or `red`
- Critical count
- Warn count
- Info count
- Public exposure conclusion
- Dangerous local actions conclusion

## Automatic Fixes Applied

List only the safe low-risk changes that were actually made during this run.
If none were made, say so briefly.

## Notes

Use this section for useful context that is not itself a finding, such as:

- gateway not currently listening
- paired-device count
- built-in audit completed successfully

## Findings

For each finding, include:

- Severity
- Check ID or short label
- Plain-language detail
- Remediation

Order findings from highest severity to lowest severity.

## Manual Actions

List only the items the user still needs to do manually.
When possible, include exact PowerShell or OpenClaw commands.

## Verification Commands

Include a short command block with the most relevant follow-up checks, usually:

- rerun the built-in audit
- inspect listeners
- inspect paired devices
- inspect ACLs when relevant
