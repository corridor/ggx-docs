import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const DOCS_DIR = path.join(process.cwd(), "src/content/docs");
const DOC_EXTENSIONS = new Set([".md", ".mdx"]);
const SITE_TITLE = "Corridor GGX Documentation";
const SITE_DESCRIPTION =
  "Documentation for Corridor GenGuardX, a Responsible AI governance platform for testing, approving, monitoring, and governing GenAI systems.";

export function llmsIntegration({ site, base = "/" }) {
  return {
    name: "ggx-llms",
    hooks: {
      "astro:build:done": async ({ dir }) => {
        const pages = await collectPages({ site, base });

        await Promise.all([
          writeLlmsTxt(dir, pages),
          writeLlmsFullTxt(dir, pages),
          writeLlmsJson(dir, pages),
          writePageMarkdown(dir, pages),
        ]);
      },
    },
  };
}

async function collectPages({ site, base }) {
  const files = await walk(DOCS_DIR);
  const pages = [];

  for (const filePath of files) {
    if (!DOC_EXTENSIONS.has(path.extname(filePath))) continue;

    const source = await readFile(filePath, "utf8");
    const relativePath = path.relative(DOCS_DIR, filePath);
    const route = routeFromContentPath(relativePath);
    const { frontmatter, body } = parseFrontmatter(source);
    const title = frontmatter.title || titleFromRoute(route);
    const description = frontmatter.description || "";
    const url = absoluteUrl(route, site, base);
    const markdownUrl = absoluteUrl(markdownRoute(route), site, base);
    const sourcePath = path.relative(process.cwd(), filePath);
    const content = normalizeContent(body);

    pages.push({
      title,
      description,
      route,
      url,
      markdownRoute: markdownRoute(route),
      markdownUrl,
      sourcePath,
      content,
    });
  }

  return pages.sort((a, b) => a.route.localeCompare(b.route));
}

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const results = [];

  for (const entry of entries) {
    const entryPath = path.join(directory, entry.name);

    if (entry.isDirectory()) {
      results.push(...(await walk(entryPath)));
    } else if (entry.isFile()) {
      results.push(entryPath);
    }
  }

  return results;
}

function parseFrontmatter(source) {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);

  if (!match) {
    return { frontmatter: {}, body: source };
  }

  return {
    frontmatter: parseFrontmatterBlock(match[1]),
    body: source.slice(match[0].length),
  };
}

function parseFrontmatterBlock(block) {
  const frontmatter = {};

  for (const line of block.split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;

    frontmatter[match[1]] = stripQuotes(match[2].trim());
  }

  return frontmatter;
}

function stripQuotes(value) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }

  return value;
}

function normalizeContent(body) {
  return body
    .replace(/^import\s.+?;\s*$/gm, "")
    .replace(/^export\s.+?;\s*$/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function routeFromContentPath(relativePath) {
  const parsed = path.parse(relativePath);
  const parts = parsed.dir ? parsed.dir.split(path.sep) : [];

  if (parsed.name !== "index") {
    parts.push(parsed.name);
  }

  return parts.length === 0 ? "/" : `/${parts.join("/")}/`;
}

function markdownRoute(route) {
  return route === "/" ? "/index.md" : `${route}index.md`;
}

function titleFromRoute(route) {
  if (route === "/") return "Overview";

  const lastSegment = route.split("/").filter(Boolean).at(-1) || "Overview";

  return lastSegment
    .split(/[-_]/)
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

function normalizeBase(base) {
  if (!base || base === "/") return "/";

  return `/${base.replace(/^\/|\/$/g, "")}/`;
}

function publicPath(route, base) {
  const normalizedBase = normalizeBase(base);
  const routePath = route.replace(/^\//, "");

  return `${normalizedBase}${routePath}`.replace(/\/{2,}/g, "/");
}

function absoluteUrl(route, site, base) {
  const origin = site.endsWith("/") ? site : `${site}/`;
  return new URL(publicPath(route, base).replace(/^\//, ""), origin).href;
}

function pageMarkdown(page) {
  return [
    `# ${page.title}`,
    "",
    `Source: ${page.url}`,
    `Markdown: ${page.markdownUrl}`,
    page.description ? `Description: ${page.description}` : "",
    "",
    page.content,
    "",
  ]
    .filter(Boolean)
    .join("\n");
}

async function writeLlmsTxt(dir, pages) {
  const lines = [
    `# ${SITE_TITLE}`,
    "",
    `> ${SITE_DESCRIPTION}`,
    "",
    "## LLM resources",
    "",
    "- [Full documentation](./llms-full.txt): Complete docs content in one Markdown-oriented text file.",
    "- [Structured index](./llms.json): Machine-readable list of docs pages and Markdown URLs.",
    "",
    "## Documentation pages",
    "",
  ];

  for (const page of pages) {
    const suffix = page.description ? `: ${page.description}` : "";
    lines.push(`- [${page.title}](${page.url})${suffix}`);
    lines.push(`  - Markdown: ${page.markdownUrl}`);
  }

  await writeFile(new URL("llms.txt", dir), `${lines.join("\n")}\n`);
}

async function writeLlmsFullTxt(dir, pages) {
  const sections = [
    `# ${SITE_TITLE}`,
    "",
    SITE_DESCRIPTION,
    "",
    "This file concatenates the public documentation pages for LLM and agent workflows.",
    "",
  ];

  for (const page of pages) {
    sections.push("---", "", pageMarkdown(page));
  }

  await writeFile(new URL("llms-full.txt", dir), `${sections.join("\n")}\n`);
}

async function writeLlmsJson(dir, pages) {
  const payload = {
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    pages: pages.map(
      ({ title, description, route, url, markdownUrl, sourcePath }) => ({
        title,
        description,
        route,
        url,
        markdown_url: markdownUrl,
        source_path: sourcePath,
      }),
    ),
  };

  await writeFile(new URL("llms.json", dir), `${JSON.stringify(payload, null, 2)}\n`);
}

async function writePageMarkdown(dir, pages) {
  await Promise.all(
    pages.map(async (page) => {
      const outputUrl = new URL(page.markdownRoute.replace(/^\//, ""), dir);
      const outputDirectoryUrl = new URL("./", outputUrl);

      await mkdir(outputDirectoryUrl, { recursive: true });
      await writeFile(outputUrl, pageMarkdown(page));
    }),
  );
}
