import { execFileSync } from "node:child_process";
import path from "node:path";

const DOCS_DIR = "src/content/docs";
const BULK_COMMIT_FILES = 15;

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

  // Group files by commit, then skip bulk commits (renames, reformatting, mass edits): they touch
  // pages without changing their content and would give many pages the same misleading date.
  const commits = [];
  for (const line of log.split("\n")) {
    if (line.startsWith("@")) {
      commits.push({ date: line.slice(1), files: [] });
    } else if (/\.mdx?$/.test(line) && commits.length > 0) {
      commits[commits.length - 1].files.push(line);
    }
  }

  for (const { date, files } of commits) {
    if (files.length > BULK_COMMIT_FILES) continue;
    for (const file of files) {
      const route = routeFromSource(file);
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
