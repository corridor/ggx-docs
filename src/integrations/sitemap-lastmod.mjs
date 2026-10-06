import { execFileSync } from "node:child_process";
import path from "node:path";

const DOCS_DIR = "src/content/docs";

// Map each docs route to the date of the last commit that touched its source file, so the
// sitemap can tell crawlers which pages actually changed.
export function gitLastModified() {
  const dates = new Map();
  let log = "";

  try {
    log = execFileSync("git", ["log", "--format=@%cI", "--name-only", "--", DOCS_DIR], {
      encoding: "utf8",
      maxBuffer: 64 * 1024 * 1024,
    });
  } catch {
    return dates;
  }

  let date = "";
  for (const line of log.split("\n")) {
    if (line.startsWith("@")) {
      date = line.slice(1);
    } else if (/\.mdx?$/.test(line)) {
      const route = routeFromSource(line);
      // Log output is newest first; keep the first date seen for each route.
      if (!dates.has(route)) dates.set(route, date);
    }
  }

  return dates;
}

function routeFromSource(file) {
  const parsed = path.posix.parse(path.posix.relative(DOCS_DIR, file));
  const parts = parsed.dir ? parsed.dir.split("/") : [];
  if (parsed.name !== "index") parts.push(parsed.name);

  return parts.length === 0 ? "/" : `/${parts.join("/")}/`;
}
