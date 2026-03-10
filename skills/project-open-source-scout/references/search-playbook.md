# Search Playbook

Use this reference when the core workflow needs more detailed search phrasing, comparison criteria, or a reusable reporting structure.

## Query Design

Build search queries from four angles:

1. Outcome
   - What the product does for the user
   - Example: `ai generated interactive landing page`
2. Category
   - What kind of product it is
   - Example: `browser start page`, `new tab page`, `ai website builder`
3. Feature
   - What makes it special
   - Example: `real-time ui generation`, `interactive blocks`, `prompt to website`
4. Stack
   - Optional technology narrowing
   - Example: `react`, `nextjs`, `electron`, `chrome extension`

## GitHub Query Patterns

Start broad, then narrow:

- `<idea>`
- `<idea> open source`
- `<idea> github`
- `<category> <feature>`
- `<category> <feature> open source`
- `<category> <feature> react`
- `<category> <feature> nextjs`
- `<category> starter`
- `<category> template`
- `awesome <category>`

## Web Search Patterns

Use web search to distinguish between:

- existing products with no reusable code
- open-source projects with weak SEO
- adjacent tools worth using as inspiration

Useful searches:

- `<idea> product`
- `<idea> demo`
- `<idea> launch`
- `<idea> open source`
- `<category> showcase`
- `<category> alternative open source`

## YouTube Search Patterns

Use YouTube when UI behavior is the main differentiator or when the product is easier to understand by watching it.

Useful searches:

- `<idea> demo`
- `<category> walkthrough`
- `<category> open source`
- `<product name> review`
- `<product name> clone`

## Candidate Scoring

Score candidates qualitatively against these checks:

- `fit`: How close is it to the requested result?
- `reuse potential`: Can it be cloned and meaningfully extended?
- `license`: Is the license present and acceptable?
- `freshness`: Is it actively maintained or at least not obviously abandoned?
- `runnability`: Are there install steps, docs, or demo deployments?
- `quality`: Does the implementation look like a stable base rather than a toy?

Use the score to decide:

- High fit + high reuse potential -> recommend clone or fork
- Medium fit + solid architecture -> recommend adapt as a base
- High inspiration + low reuse potential -> keep as reference only
- Low fit or unclear license -> reject

## Report Template

Use this compact structure when the user needs a decision fast:

```text
Project Brief
- Idea:
- Assumptions:
- Must-have features:

Search Summary
- Sources searched:
- Query angles:
- What looked promising:

Best Reusable Candidates
1. Name / link
   Why it matters:
   Classification:
   Risks:

Decision
- clone / adapt / build from scratch
- Why:

Next Action
- immediate step
```

## Example: AI Browser UI Idea

For a request like:

`Build a clean browser UI with no ad-like clutter, plus an embedded AI that generates interactive UI pages from user requests.`

Start with queries such as:

- `ai generated browser start page open source`
- `prompt to landing page open source`
- `interactive ai website builder github`
- `ai ui generator react open source`
- `new tab ai landing page github`

Then separate findings into:

- open-source repos that can be cloned
- closed-source products that only inform product direction
- UI inspirations with no reusable implementation
