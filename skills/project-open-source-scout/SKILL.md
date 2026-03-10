---
name: project-open-source-scout
description: Research whether a proposed project already has reusable open-source implementations before starting new development. Use when the user first describes a project idea, feature set, product concept, UI direction, app, workflow, or MVP and wants Codex to search GitHub, the web, and YouTube for similar repos, templates, demos, or near-matches, then decide whether to clone and adapt an existing project or build from scratch. Trigger on requests such as "I want to build a project", "search for similar open-source projects first", "check GitHub for existing repos", "see whether we can pull something ready-made", or any early-stage reuse-first project discovery request.
---

# Project Open Source Scout

Use this skill at the beginning of a project to avoid rebuilding work that already exists. Prefer reuse when a credible open-source base exists, and switch to greenfield implementation only when the search result does not justify reuse.

Read [references/search-playbook.md](references/search-playbook.md) only when you need detailed query patterns, candidate scoring heuristics, or a ready-made scouting report structure.

## Default Behavior

- Treat the user's first project description as a reuse-first scouting brief.
- Clarify only the minimum details needed to search well: target platform, must-have features, hard constraints, and any licensing or business restrictions.
- When low-risk details are missing, make a reasonable assumption, state it, and continue searching instead of blocking.
- Search sources in this order:
  - GitHub and other code hosts for reusable repositories
  - The wider web for product pages, showcases, blog posts, and launch pages
  - YouTube for interaction demos when the request depends on live UI behavior
- Separate findings into:
  - `directly reusable repo`
  - `adaptable base`
  - `inspiration only`
  - `closed-source / not usable`
- Prefer open-source projects with a license, recent activity, install or run evidence, and clear alignment with the requested idea.
- Check license fit before recommending direct reuse for commercial or productized work.
- Do not confuse visual inspiration with a codebase that can actually be cloned and used.

## Workflow

### 1. Normalize the project brief

- Extract the product category, target users, platform, core interactions, and non-negotiable constraints.
- Convert the brief into a short search target:
  - one-sentence project summary
  - 3-7 must-have features
  - useful synonyms
  - likely technical keywords
- If the user names a stack, include it in search variations. If not, search stack-agnostic first.

### 2. Hunt for candidates

- Search for exact matches first using the core idea wording.
- Expand into broader variations, adjacent terms, and framework-specific searches.
- Search GitHub for:
  - exact project phrasing
  - category and feature combinations
  - framework variants such as `react`, `nextjs`, `vue`, `electron`, `browser`, `landing page`, `ai ui`
  - curated lists and starter kits
- Search the web for:
  - product launches
  - showcase articles
  - demo sites
  - founders describing similar products
- Search YouTube only when visual behavior matters or when a project seems real but the repo is unclear.

### 3. Evaluate each candidate

For each strong candidate, check:

- How closely it matches the requested outcome
- Whether the repository is truly open-source
- License suitability
- Maintenance freshness
- Demo or screenshot quality
- Whether setup instructions or deploy guidance exist
- Whether the architecture seems usable as a base instead of a throwaway demo

Classify the result:

- `direct fit`: Covers most must-have requirements and is practical to reuse now
- `adaptable base`: Solves a meaningful part of the problem, but needs custom work
- `inspiration only`: Useful for product direction or UX ideas, but not for cloning
- `not usable`: Low quality, abandoned, missing license, or not actually relevant

## Decision Rules

- Choose `clone/adapt existing project` when one repo covers most of the required behavior and the license is acceptable.
- Choose `start from an adaptable base` when no exact match exists but one project clearly reduces build time.
- Choose `build from scratch` when:
  - no credible open-source implementation exists
  - only closed-source examples exist
  - licensing blocks reuse
  - the available repos are too weak, outdated, or off-target
- When a similar closed-source product exists but no open repository exists, explicitly say that it is reference material only and should not block a custom build.

## Response Format

Use this structure when reporting results:

- `Project Brief`: Restate the idea and assumptions
- `Search Summary`: Explain where you searched and what patterns you used
- `Best Reusable Candidates`: List the strongest repos or references with a one-line reason
- `Decision`: State `clone`, `adapt`, or `build from scratch`
- `Next Action`: Give the immediate next step, such as clone a repo, inspect license, or start implementation

## Operating Rules

- Bias toward saving the user time, not toward forcing originality.
- Prefer one strong recommendation over a long list of weak links.
- Explain why a candidate is reusable, not just that it looks similar.
- Surface the license status whenever it affects the recommendation.
- If the user asks to proceed after the scouting step, continue from the chosen path instead of repeating the search.
- If the search is blocked by environment limits, say what was blocked and what should be checked next.

## Example Requests

- `I want to build a project. First search GitHub for similar open-source repos we can clone.`
- `Before we build this browser UI idea, search for open-source projects or demos that already do something close.`
- `Check whether this product idea already has a repo we can reuse before starting from scratch.`
