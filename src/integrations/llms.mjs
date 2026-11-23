import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const DOCS_DIR = path.join(process.cwd(), "src/content/docs");
const DOC_EXTENSIONS = new Set([".md", ".mdx"]);
const SITE_TITLE = "GGX Documentation";
const JUDGES_DIR = path.join(process.cwd(), "src/data/llm-judges");
// Top-level route segments, in sidebar order, used to group llms.txt.
const SECTIONS = [
  ["register-and-refine", "Register and Refine"],
  ["evaluate-and-approve", "Evaluate and Approve"],
  ["deploy-and-monitor", "Deploy and Monitor"],
  ["integrations", "Integrations"],
  ["technology", "Technology"],
  ["llm-judges", "LLM Judges"],
  ["faq", "FAQ"],
];
const SITE_DESCRIPTION =
  "Documentation for GenGuardX, a Responsible AI governance platform for testing, approving, monitoring, and governing GenAI systems.";

export function llmsIntegration({ site, base = "/" }) {
  return {
    name: "ggx-llms",
    hooks: {
      // The per-page Markdown files only exist after a build; serve them on the fly in dev
      // so the "View Markdown" and "Ask AI" links work there too.
      "astro:server:setup": ({ server }) => {
        server.middlewares.use(async (req, res, next) => {
          const pathname = decodeURIComponent((req.url || "").split(/[?#]/)[0]);
          if (!pathname.endsWith("/index.md")) return next();

          try {
            const pages = await collectPages({ site, base });
            const page = pages.find(
              (candidate) => publicPath(candidate.markdownRoute, base) === pathname,
            );
            if (!page) return next();

            res.setHeader("Content-Type", "text/markdown; charset=utf-8");
            res.end(pageMarkdown(page));
          } catch (error) {
            next(error);
          }
        });
      },
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
  const judges = await judgesMarkdown();
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
    const content = normalizeContent(body, { url, site, base, judges });

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

function normalizeContent(body, context) {
  // Fenced code is copied through untouched; only prose is converted.
  const converted = body
    .split(/(^[ \t]*(?:```|~~~)[\s\S]*?^[ \t]*(?:```|~~~)[ \t]*$)/m)
    .map((segment, index) => (index % 2 ? segment : proseToMarkdown(segment, context)))
    .join("");

  return converted.replace(/\n{3,}/g, "\n\n").trim();
}

// Turn MDX components, JSX, and Starlight directives into plain Markdown so the output is
// readable by LLMs and by people opening "View Markdown".
function proseToMarkdown(source, { url, site, base, judges }) {
  let text = source
    .replace(/^import\s.+?;\s*$/gm, "")
    .replace(/^export\s.+?;\s*$/gm, "")
    .replace(
      /\{`\$\{import\.meta\.env\.BASE_URL\}([^`]*)`\}/g,
      (_, route) => `"${absoluteUrl(`/${route}`, site, base)}"`,
    );

  text = replaceComponent(text, "LlmJudges", () => judges);
  text = replaceComponent(text, "BenchmarkBarChart", chartMarkdown);
  text = replaceComponent(text, "LinkCard", ({ title, description, href }) =>
    `- [${title}](${href})${description ? `: ${description}` : ""}`,
  );
  text = replaceComponent(text, "Badge", ({ text: label }) => `(${label})`);

  text = text
    .replace(
      /<LinkButton\s[^>]*?href="([^"]*)"[^>]*>\s*([\s\S]*?)\s*<\/LinkButton>/g,
      "[$2]($1)",
    )
    .replace(/<a\s[^>]*?href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g, "[$2]($1)")
    .replace(/<video[\s\S]*?src="([^"]*)"[\s\S]*?<\/video>/g, "[Video]($1)")
    .replace(/<figcaption>([\s\S]*?)<\/figcaption>/g, "*$1*")
    .replace(/^[ \t]*<Card\s[^>]*?title="([^"]*)"[^>]*>[ \t]*(\S.*?)<\/Card>[ \t]*$/gm, "- **$1**: $2")
    .replace(/<(?:Card|Aside)\s[^>]*?title="([^"]*)"[^>]*>/g, "**$1**\n")
    .replace(/<TabItem\s[^>]*?label="([^"]*)"[^>]*>/g, "**$1**\n")
    .replace(/^[ \t]*<\/?(?:Tabs|TabItem|CardGrid|Card|Steps|Aside|figure|helper-panel)(?:\s[^>]*)?>[ \t]*$/gm, "")
    // Remaining presentational JSX wrappers: keep their text, drop the markup and indentation.
    .replace(/^[ \t]*(?:<\/?(?:div|span)(?:\s(?:[^>{]|\{\{[^}]*\}\}|\{[^}]*\})*)?>[ \t]*)+$/gm, "")
    .replace(/^[ \t]*<(div|span)(?:\s(?:[^>{]|\{\{[^}]*\}\}|\{[^}]*\})*)?>(.*?)<\/\1>[ \t]*$/gm, (_, tag, inner) =>
      tag === "span" ? `- ${inner}` : `${inner}\n`,
    )
    .replace(/&amp;/g, "&")
    .replace(/^[ \t]+(?=<(?:h[1-6]|p)[ >])/gm, "")
    .replace(/<h([1-6])[^>]*>(.*?)<\/h\1>/g, (_, level, heading) => `${"#".repeat(Number(level))} ${heading}`)
    .replace(/<p(?:\s(?:[^>{]|\{\{[^}]*\}\}|\{[^}]*\})*)?>([\s\S]*?)<\/p>/g, (_, paragraph) =>
      paragraph.replace(/\s*\n\s*/g, " ").trim(),
    )
    // Starlight asides: `:::tip[Title]` ... `:::`
    .replace(/^([ \t]*):::(\w+)(?:\[(.*?)\])?[ \t]*$/gm, (_, indent, type, title) => {
      const label = type.charAt(0).toUpperCase() + type.slice(1);
      return `${indent}**${title ? `${label}: ${title}` : label}**\n`;
    })
    .replace(/^[ \t]*:::[ \t]*$/gm, "")
    // Images are fingerprinted at build time, so keep the description instead of a dead path.
    .replace(/!\[([^\]]*)\]\((?!https?:)[^)]*\)/g, (_, alt) => (alt ? `*Figure: ${alt}*` : ""))
    // Resolve relative and root-relative links against the published page URL.
    .replace(/(?<!!)\[([^\]]+)\]\((?!https?:|mailto:|#)([^)\s]+)\)/g, (_, label, href) => {
      const target = href.startsWith("/")
        ? absoluteUrl(href.slice(normalizeBase(base).length - 1) || "/", site, base)
        : new URL(href, url).href;
      return `[${label}](${target})`;
    });

  return text;
}

// Replace every `<Name ... />` with the output of `render(props)`. Attribute values may be
// quoted strings or `{expressions}` containing nested braces.
function replaceComponent(text, name, render) {
  let output = "";
  let cursor = 0;

  for (;;) {
    const start = text.indexOf(`<${name}`, cursor);
    if (start === -1 || !/[\s/>]/.test(text[start + name.length + 1] ?? "")) {
      if (start === -1) break;
      output += text.slice(cursor, start + 1);
      cursor = start + 1;
      continue;
    }

    const props = {};
    let index = start + name.length + 1;
    let depth = 0;
    let quote = "";
    let attributeStart = index;

    for (; index < text.length; index += 1) {
      const char = text[index];
      if (quote) {
        if (char === quote) quote = "";
      } else if (char === '"' || char === "'" || char === "`") {
        quote = char;
      } else if (char === "{") {
        depth += 1;
      } else if (char === "}") {
        depth -= 1;
      } else if (char === ">" && depth === 0) {
        break;
      }
    }

    const attributes = text.slice(attributeStart, index).replace(/\/\s*$/, "");
    const pattern = /([A-Za-z]+)=(?:"([^"]*)"|\{)/g;
    let match;
    while ((match = pattern.exec(attributes))) {
      if (match[2] !== undefined) {
        props[match[1]] = match[2];
        continue;
      }
      let end = pattern.lastIndex;
      for (let level = 1; end < attributes.length && level > 0; end += 1) {
        if (attributes[end] === "{") level += 1;
        if (attributes[end] === "}") level -= 1;
      }
      props[match[1]] = attributes.slice(pattern.lastIndex, end - 1);
      pattern.lastIndex = end;
    }

    output += text.slice(cursor, start) + render(props);
    cursor = index + 1;
  }

  return output + text.slice(cursor);
}

function chartMarkdown({ title, description, series, data }) {
  try {
    // Chart props are object literals authored in this repository's own MDX.
    const columns = new Function(`return (${series});`)();
    const rows = new Function(`return (${data});`)();
    const lines = [
      `**${title}** — ${description}`,
      "",
      `| | ${columns.map((column) => column.label).join(" | ")} |`,
      `| --- | ${columns.map(() => "---").join(" | ")} |`,
      ...rows.map(
        (row) =>
          `| ${row.label} | ${columns
            .map((column) => row.display?.[column.key] ?? row.values[column.key] ?? "")
            .join(" | ")} |`,
      ),
    ];
    return lines.join("\n");
  } catch {
    return `**${title}** — ${description}`;
  }
}

// The judge gallery is rendered by a component, so list the same data as Markdown.
async function judgesMarkdown() {
  const entries = await readdir(JUDGES_DIR, { withFileTypes: true }).catch(() => []);
  const judges = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const directory = path.join(JUDGES_DIR, entry.name);
    const meta = JSON.parse(await readFile(path.join(directory, "meta.json"), "utf8"));
    const read = (file) => readFile(path.join(directory, file), "utf8").catch(() => "");
    judges.push({
      ...meta,
      prompt: await read(meta.promptFile ?? "prompt.txt"),
      code: await read(meta.module ?? "judge.py"),
    });
  }

  return judges
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((judge) =>
      [
        `### ${judge.name}`,
        "",
        `- Category: ${judge.category}`,
        judge.scoreRange ? `- Score range: ${judge.scoreRange}` : "",
        judge.tags?.length ? `- Tags: ${judge.tags.join(", ")}` : "",
        "",
        judge.description || judge.summary || "",
        "",
        // Most judges embed the prompt in their module; avoid printing it twice.
        ...(judge.code.includes(judge.prompt.trim().slice(0, 200))
          ? []
          : ["Prompt:", "", `~~~text\n${judge.prompt.trim()}\n~~~`, ""]),
        "Code:",
        "",
        `~~~python\n${judge.code.trim()}\n~~~`,
      ]
        .filter((line, index, lines) => line !== "" || lines[index - 1] !== "")
        .join("\n"),
    )
    .join("\n\n");
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
  ]
    .filter(Boolean)
    .concat("", page.content, "")
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
    "## Overview",
    "",
  ];

  const entry = (page) => {
    const suffix = page.description ? `: ${page.description}` : "";
    return [`- [${page.title}](${page.url})${suffix}`, `  - Markdown: ${page.markdownUrl}`];
  };
  const sectionOf = (page) => page.route.split("/")[1] || "";
  const known = new Set(SECTIONS.map(([segment]) => segment));

  lines.push(...pages.filter((page) => !known.has(sectionOf(page))).flatMap(entry));

  for (const [segment, label] of SECTIONS) {
    const sectionPages = pages.filter((page) => sectionOf(page) === segment);
    if (sectionPages.length === 0) continue;

    lines.push("", `## ${label}`, "", ...sectionPages.flatMap(entry));
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
