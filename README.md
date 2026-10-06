# GenGuardX Documentation

Documentation site for GenGuardX ("GGX"), built with [Astro Starlight](https://starlight.astro.build/).

## Prerequisites

- Node.js 20+ (22 recommended)

## Local development

Install dependencies and start the dev server with live reload:

    npm install
    npm run dev

The site is served at <http://localhost:4321>.

## Building the site

    npm run build

This outputs the static site to `dist/` with the site root (`/`).

## Deployment

Pushing to `main` triggers two workflows, each of which builds the site with base URL `/`:

- [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) publishes the test site to
  GitHub Pages at <https://docs.test.genguardx.ai> with a noindex `robots.txt`.
- [`.github/workflows/deploy-prod.yml`](.github/workflows/deploy-prod.yml) syncs the build to
  the production server behind <https://docs.genguardx.ai> over SSH, then checks that the
  site responds and is still indexable. It can also be run manually from the Actions tab.

> The repository's **Settings → Pages → Source** must be set to **GitHub Actions**.

The production workflow runs in the `production` environment, which must define these secrets:

| Secret | Value |
| --- | --- |
| `PROD_SSH_HOST` | Address of the production server |
| `PROD_SSH_PRIVATE_KEY` | Private key of a deploy user that can run `sudo rsync` |
| `PROD_SSH_KNOWN_HOSTS` | The server's `known_hosts` line, from `ssh-keyscan <host>` |
| `PROD_AWS_ROLE_ARN` | IAM role the workflow assumes through GitHub OIDC |
| `PROD_SECURITY_GROUP_ID` | Empty security group attached only to the production server |

The server does not accept SSH from GitHub's runners, so the workflow uses the IAM role to
allow the runner's IP on port 22 for the length of the sync and removes the rule afterwards.

Add required reviewers to the `production` environment to require approval before each
production deployment.

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

- Avoid using "the platform" and instead use "GenGuardX" so readers are clear on what
  is being said.
- Run a grammar/spell check on the content to fix any grammar issues and typos.
