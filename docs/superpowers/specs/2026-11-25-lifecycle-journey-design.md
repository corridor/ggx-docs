# Home page lifecycle journey (design)

## Intent
Show the six-stage GGX lifecycle on the docs home page, as the website does, so a reader sees the journey and
what the platform offers at each stage and can jump to the right page. Requested by the user; modelled on the
"From idea to production" section of the Claude platform docs.

## Goals
- Six numbered stages with a short title and a row of link cards each: 1 Build & Connect, 2 Business Confidence,
  3 Risk Approval, 4 Deployment, 5 Monitoring, 6 Re-evaluate. Names and order match the website.
- Cards link only to pages that already exist. No new content pages.
- Matches the site theme in light and dark, works at phone width, and adds no client JavaScript.

## Non-goals
- No tabs (one lifecycle, not two products). No sidebar, URL or redirect changes. No removal of the existing
  home page text, which carries the SEO content.

## Anti-goals
- Cards that point to missing pages, or a page that is slower to load or looks different from the rest of the site.

## Approaches
1. **Journey above the existing home page (chosen).** Smallest change; keeps SEO text; longer page.
2. Journey replaces the narrative, which moves to an "About GGX" page. Cleaner, but loses indexed text on `/`.
3. Journey plus renaming the sidebar topics to the six stages. Most consistent, but changes URLs and needs redirects.

## Design
- New static component `src/components/LifecycleJourney.astro` (same style as `IntegrationShowcase.astro`):
  a `stages` array of `{ number, title, cards: [{ title, href, icon }] }`, rendered as a vertical numbered
  timeline with a card grid per stage. Theme variables only (`--sl-color-*`), icons from Starlight's `Icon`.
- Rendered in `src/content/docs/index.mdx` directly under the opening paragraph, before the video.
- Cards (first draft, builder to confirm each link resolves):
  1. Build & Connect: Register agents, models, prompts and datasets; Integrations; Sync and SDK; Project templates
  2. Business Confidence: Feedback portals; Testing plan; Generate tests with Corra; Get feedback from an expert
  3. Risk Approval: Risk assessment; Approval workflows; Reporting; LLM judges
  4. Deployment: Direct to production; Deployment platforms; Deployment jobs
  5. Monitoring: Monitoring and performance; Annotation queues; Oversight
  6. Re-evaluate: Rerun reports; Compare versions; Prompt optimization; Version management
- A separate strip under the stages for what cuts across all of them: Corra AI, Administration, Developers.
- Every card has a visible label; the timeline is a list (`ul`/`ol`) for screen readers; headings keep the
  page's heading order.

## Checks
`npm run build` passes; a script confirms every card `href` resolves to a built page; view at desktop and phone
width in light and dark.

## Left to the builder
Exact card wording, icon choices, and spacing, following the existing components.
