# Corridor Documentation

Documentation site for Corridor GenGuardX ("GGX"), built with [Astro Starlight](https://starlight.astro.build/).

## Prerequisites

- Node.js 20+ (22 recommended)
- Python 3.10+ — only needed to build and serve the offline `corridor-docs` package

## Local development

Install dependencies and start the dev server with live reload:

    npm install
    npm run dev

The site is served at <http://localhost:4321>.

## Building the site

    npm run build

This outputs the static site to `corridor_docs/site/` with the site root (`/`).

## Serving the offline (Flask) package

The built site is packaged into the `corridor_docs` Python package and can be served
offline (e.g. for self-hosted / air-gapped installs):

    # 1. build the site (base must be '/')
    npm run build

    # 2. install and serve
    uv venv venv --python 3.11 --seed
    uv pip install -e . --python venv
    venv/bin/corridor-docs run

The docs are then served at <http://localhost:5005>.

## Deployment

Pushing to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml),
which builds the site with base URL `/` and publishes it to GitHub Pages.

> The repository's **Settings → Pages → Source** must be set to **GitHub Actions**.

## Authoring content

- Content lives in `src/content/docs/` as Markdown (`.md`) or MDX (`.mdx`).
- Navigation/sidebar order is configured in [`astro.config.mjs`](astro.config.mjs).
- Every page needs a `title` in its frontmatter.
- Use Starlight asides for callouts: `:::note`, `:::tip`, `:::caution`, `:::danger`.
- For richer layouts (tabs, card grids) use MDX with Starlight components such as
  `<Tabs>`, `<TabItem>`, `<CardGrid>`, and `<Card>`.
- Co-locate images next to the page that uses them and reference them with relative
  paths so Astro can optimize them.

### Writing guidelines

- Avoid using "the platform" and instead use "Corridor" so readers are clear on what
  is being said.
- Run a grammar/spell check on the content to fix any grammar issues and typos.
