# Home page lifecycle journey Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a six-stage lifecycle journey of link cards to the top of the docs home page.

**Architecture:** One static Astro component holds the stage data and markup; `index.mdx` imports and renders it
under the opening paragraph. No client JavaScript.

**Tech Stack:** Astro Starlight, `@astrojs/starlight/components` `Icon`.

**Spec:** `docs/superpowers/specs/2026-11-25-lifecycle-journey-design.md`

## Global Constraints
- Stage names and order: 1 Build & Connect, 2 Business Confidence, 3 Risk Approval, 4 Deployment, 5 Monitoring, 6 Re-evaluate.
- Cards link only to existing pages. Theme variables only (`--sl-color-*`). Works at phone width, light and dark.
- No tabs, no sidebar/URL changes, existing home text untouched.

## Review Focus
- A card `href` with a typo or missing trailing slash builds fine but 404s: the link check in Task 1 catches it.
- Unknown icon name fails the build: Task 1 build step catches it.
- Narrow screens (360px): the grid must collapse to one column with no horizontal scroll.
- Dark mode: card background and border must stay visible (use gray tokens, not hard-coded colours).
- Heading order: stage titles are `h3` under the section's `h2`, so the page outline stays valid.

---

### Task 1: LifecycleJourney component on the home page

**Files:**
- Create: `src/components/LifecycleJourney.astro`
- Modify: `src/content/docs/index.mdx` (import, and `<LifecycleJourney />` after the first paragraph)
- Test: `npm run build` plus a link check over `dist/`

**Interfaces:**
- Produces: `<LifecycleJourney />`, no props. Data: `stages: { title: string; cards: { title: string; href: string; icon: string }[] }[]`
  and `across: { title; href; icon }[]`.

- [ ] Step 1: Write the component with the stage and card data from the spec, an `h2` "From build to production"
  with a one-line intro, an `ol` of stages (number badge, `h3` title, `ul` card grid), and the cross-cutting strip.
- [ ] Step 2: Import and render it in `index.mdx`.
- [ ] Step 3: Run `npm run build`; expect "194 page(s) built" and no `[ERROR]`.
- [ ] Step 4: Link check: every `href` in the component resolves to `dist/<href>index.html`; expect zero missing.
- [ ] Step 5: View the built home page at 1440px and 375px, light and dark; no overflow, cards readable.
- [ ] Step 6: Commit the component, `index.mdx`, the spec and this plan.
