#!/usr/bin/env node
import fs from "node:fs";
import { execFileSync } from "node:child_process";
import process from "node:process";

const DEFAULT_CANONICAL = "oaslananka-lab/kicad-mcp-pro";
const DEFAULT_PERSONAL = "oaslananka/kicad-mcp-pro";
const PACKAGE_NAME = "kicad-mcp-pro";

function usage() {
  return `Usage: node scripts/release-state.mjs [options]

Inspect the current release state and print the next safe operation. The script
is read-only: it never publishes, deletes refs, edits releases, or pushes.

Options:
  --repo <owner/name>       Canonical repository. Default: ${DEFAULT_CANONICAL}
  --personal <owner/name>   Personal showcase repository. Default: ${DEFAULT_PERSONAL}
  --version <version>       Version or v-prefixed tag. Default: pyproject.toml version.
  --json                    Print JSON only.
  --json-out <path>         Also write the JSON payload to a file.
  --offline                 Do not query GitHub, PyPI, TestPyPI, or git remotes.
  --help                    Show this help.
`;
}

function parseArgs(argv) {
  const args = {
    repo: DEFAULT_CANONICAL,
    personal: DEFAULT_PERSONAL,
    json: false,
    offline: false,
    jsonOut: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else if (arg === "--json") {
      args.json = true;
    } else if (arg === "--offline") {
      args.offline = true;
    } else if (["--repo", "--personal", "--version", "--json-out"].includes(arg)) {
      const value = argv[index + 1];
      if (!value) throw new Error(`${arg} requires a value`);
      args[arg.slice(2).replace(/-([a-z])/g, (_, char) => char.toUpperCase())] = value;
      index += 1;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return args;
}

function splitRepo(repo) {
  const parts = repo.split("/");
  if (parts.length !== 2 || !parts[0] || !parts[1]) {
    throw new Error(`Repository must be owner/name, got ${repo}`);
  }
  return { owner: parts[0], name: parts[1] };
}

function readPyprojectVersion() {
  const content = fs.readFileSync("pyproject.toml", "utf8");
  const match = content.match(/^version\s*=\s*"([^"]+)"/m);
  if (!match) throw new Error("pyproject.toml project.version was not found");
  return match[1];
}

function readJsonVersion(path) {
  if (!fs.existsSync(path)) return null;
  const data = JSON.parse(fs.readFileSync(path, "utf8"));
  if (typeof data.version === "string") return data.version;
  const packageVersion = data.packages?.find?.((entry) => typeof entry?.version === "string")?.version;
  return packageVersion || null;
}

function normalizeVersion(input) {
  const version = (input || readPyprojectVersion()).trim().replace(/^v/, "");
  if (!/^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(version)) {
    throw new Error(`Version must be semantic and may be v-prefixed, got ${input}`);
  }
  return version;
}

function headers() {
  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
  return {
    accept: "application/vnd.github+json",
    "x-github-api-version": "2022-11-28",
    ...(token ? { authorization: `Bearer ${token}` } : {}),
  };
}

async function getJson(url, requestHeaders = {}) {
  const response = await fetch(url, { headers: { "user-agent": "release-state-script", accept: "application/json", ...requestHeaders } });
  if (response.status === 404) return { found: false, status: 404 };
  if (!response.ok) {
    return { found: false, status: response.status, error: `${response.status} ${response.statusText}` };
  }
  const body = await response.json();
  return { found: true, status: response.status, body };
}

async function githubJson(repo, path) {
  return getJson(`https://api.github.com/repos/${repo}${path}`, headers());
}

async function pypiState(index, version) {
  const base = index === "PyPI" ? "https://pypi.org" : "https://test.pypi.org";
  const response = await getJson(`${base}/pypi/${PACKAGE_NAME}/${version}/json`);
  const files = response.found ? response.body.urls || [] : [];
  return {
    index,
    published: response.found,
    status: response.status,
    url: `${base}/project/${PACKAGE_NAME}/${version}/`,
    file_count: files.length,
    files: files.map((file) => ({
      filename: file.filename,
      packagetype: file.packagetype,
      python_version: file.python_version,
    })),
    error: response.error || null,
  };
}

function runGit(args) {
  try {
    return execFileSync("git", args, { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch {
    return "";
  }
}

function parseLsRemote(output) {
  const entries = new Map();
  for (const line of output.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const [sha, ref] = line.trim().split(/\s+/, 2);
    entries.set(ref, sha);
  }
  return entries;
}

function remoteUrl(repo) {
  return `https://github.com/${repo}.git`;
}

function gitRemoteRefs(repo, refs) {
  const output = runGit(["ls-remote", remoteUrl(repo), ...refs]);
  return parseLsRemote(output);
}

function localTagState(tag) {
  const tagSha = runGit(["rev-parse", "--verify", `refs/tags/${tag}^{}`]);
  return {
    exists: Boolean(tagSha),
    peeled_sha: tagSha || null,
  };
}

function inspectMirror({ canonicalRepo, personalRepo, tag, offline }) {
  if (offline) {
    return {
      checked: false,
      synced: false,
      main: { status: "offline" },
      tag: { name: tag, status: "offline" },
      divergent_tags: [],
      missing_tags: [],
    };
  }

  const canonicalRefs = gitRemoteRefs(canonicalRepo, ["refs/heads/main", `refs/tags/${tag}`]);
  const personalRefs = gitRemoteRefs(personalRepo, ["refs/heads/main", `refs/tags/${tag}`]);
  const canonicalMain = canonicalRefs.get("refs/heads/main") || null;
  const personalMain = personalRefs.get("refs/heads/main") || null;
  const canonicalTag = canonicalRefs.get(`refs/tags/${tag}`) || null;
  const personalTag = personalRefs.get(`refs/tags/${tag}`) || null;

  const mainStatus =
    canonicalMain && personalMain && canonicalMain === personalMain
      ? "synced"
      : canonicalMain && personalMain
        ? "diverged-or-behind"
        : "missing";
  const tagStatus =
    canonicalTag && personalTag && canonicalTag === personalTag
      ? "synced"
      : canonicalTag && personalTag
        ? "divergent"
        : canonicalTag
          ? "missing"
          : "canonical-tag-missing";

  return {
    checked: true,
    synced: mainStatus === "synced" && tagStatus === "synced",
    main: {
      status: mainStatus,
      canonical_sha: canonicalMain,
      personal_sha: personalMain,
    },
    tag: {
      name: tag,
      status: tagStatus,
      canonical_sha: canonicalTag,
      personal_sha: personalTag,
    },
    divergent_tags: tagStatus === "divergent" ? [tag] : [],
    missing_tags: tagStatus === "missing" ? [tag] : [],
  };
}

function summarizeRun(run) {
  if (!run) return null;
  return {
    id: run.database_id || run.id,
    name: run.name,
    display_title: run.display_title,
    event: run.event,
    status: run.status,
    conclusion: run.conclusion,
    head_branch: run.head_branch,
    head_sha: run.head_sha,
    created_at: run.created_at,
    url: run.html_url,
  };
}

async function inspectGitHub({ canonicalRepo, tag, offline }) {
  if (offline) {
    return {
      open_pr_count: null,
      open_prs: [],
      closed_release_prs: [],
      tag_ref: { exists: false, offline: true },
      github_release: { exists: false, offline: true },
      release_runs: [],
      mirror_run: null,
    };
  }

  const [pulls, closedPulls, tagRef, release, releaseRuns, mirrorRuns] = await Promise.all([
    githubJson(canonicalRepo, "/pulls?state=open&per_page=100"),
    githubJson(canonicalRepo, "/pulls?state=closed&per_page=20"),
    githubJson(canonicalRepo, `/git/ref/tags/${encodeURIComponent(tag)}`),
    githubJson(canonicalRepo, `/releases/tags/${encodeURIComponent(tag)}`),
    githubJson(canonicalRepo, "/actions/workflows/release.yml/runs?per_page=20"),
    githubJson(canonicalRepo, "/actions/workflows/mirror-personal.yml/runs?per_page=5"),
  ]);

  const openPrs = pulls.found
    ? pulls.body.map((pr) => ({
        number: pr.number,
        title: pr.title,
        draft: pr.draft,
        state: pr.state,
        url: pr.html_url,
        head: pr.head?.ref,
      }))
    : [];
  const closedReleasePrs = closedPulls.found
    ? closedPulls.body
        .filter((pr) => pr.merged_at && (pr.head?.ref?.startsWith("release-please--") || /release/i.test(pr.title)))
        .map((pr) => ({
          number: pr.number,
          title: pr.title,
          merged_at: pr.merged_at,
          url: pr.html_url,
          head: pr.head?.ref,
        }))
    : [];

  return {
    open_pr_count: pulls.found ? openPrs.length : null,
    open_prs: openPrs,
    closed_release_prs: closedReleasePrs,
    tag_ref: {
      exists: tagRef.found,
      status: tagRef.status,
      sha: tagRef.body?.object?.sha || null,
      type: tagRef.body?.object?.type || null,
      error: tagRef.error || null,
    },
    github_release: {
      exists: release.found,
      status: release.status,
      draft: release.body?.draft ?? null,
      prerelease: release.body?.prerelease ?? null,
      published_at: release.body?.published_at || null,
      url: release.body?.html_url || null,
      asset_count: release.body?.assets?.length || 0,
      error: release.error || null,
    },
    release_runs: releaseRuns.found ? releaseRuns.body.workflow_runs.map(summarizeRun) : [],
    mirror_run: mirrorRuns.found ? summarizeRun(mirrorRuns.body.workflow_runs[0]) : null,
  };
}

function latestSuccessfulDryRun(releaseRuns, tag) {
  return releaseRuns.find(
    (run) =>
      run?.conclusion === "success" &&
      (run.display_title?.includes(tag) || run.head_branch === tag),
  );
}

function decideState({ github, testpypi, pypi, mirror, metadata, version, tag }) {
  const blockers = [];
  const versions = Object.entries(metadata.versions).filter(([, value]) => value !== null);
  const uniqueVersions = new Set(versions.map(([, value]) => value));
  if (uniqueVersions.size !== 1) {
    blockers.push(
      `Release metadata version drift: ${versions.map(([name, value]) => `${name}=${value}`).join(", ")}`,
    );
  }
  if (!uniqueVersions.has(version)) {
    blockers.push(`Requested version ${version} does not match checked metadata.`);
  }
  if (!github.tag_ref.exists && !metadata.local_tag.exists) {
    blockers.push(`Version tag ${tag} is missing locally and on the canonical repository.`);
  }
  if (pypi.published && !github.github_release.exists) {
    blockers.push(`PyPI has ${version}, but the GitHub Release ${tag} was not found.`);
  }
  if (mirror.tag.status === "divergent") {
    blockers.push(
      `Personal showcase tag ${tag} diverges. Use mirror-personal.yml manual force_mirror recovery only after approval.`,
    );
  }

  let currentState = "no-release";
  if (github.open_prs.some((pr) => pr.head?.startsWith("release-please--") || /release/i.test(pr.title))) {
    currentState = "release-pr-open";
  }
  if (!github.tag_ref.exists && !metadata.local_tag.exists && github.closed_release_prs.length > 0) {
    currentState = "release-pr-merged";
  }
  if (github.tag_ref.exists || metadata.local_tag.exists) currentState = "tag-created";
  if (latestSuccessfulDryRun(github.release_runs, tag) || github.github_release.draft) {
    currentState = "dry-run-success";
  }
  if (testpypi.published) currentState = "testpypi-published";
  if (pypi.published) currentState = "pypi-published";
  if (pypi.published && mirror.synced) currentState = "mirror-synced";
  if (pypi.published && mirror.synced && github.github_release.exists && !github.github_release.draft) {
    currentState = "complete";
  }
  if (blockers.length > 0) currentState = "blocked";

  let nextSafeCommand = "Resolve blockers before running a release or mirror command.";
  if (blockers.length === 0) {
    if (!github.tag_ref.exists && !metadata.local_tag.exists) {
      nextSafeCommand = "Merge the release-please release PR and let it create the version tag.";
    } else if (!latestSuccessfulDryRun(github.release_runs, tag) && !github.github_release.exists) {
      nextSafeCommand = `gh workflow run release-controller.yml --repo ${DEFAULT_CANONICAL} -f mode=dry-run -f version=${tag}`;
    } else if (!testpypi.published) {
      nextSafeCommand = `gh workflow run release-controller.yml --repo ${DEFAULT_CANONICAL} -f mode=testpypi -f version=${tag} -f approval=APPROVE_RELEASE`;
    } else if (!pypi.published) {
      nextSafeCommand = `gh workflow run release-controller.yml --repo ${DEFAULT_CANONICAL} -f mode=pypi -f version=${tag} -f allow_pypi=true -f approval=APPROVE_RELEASE`;
    } else if (!mirror.synced) {
      nextSafeCommand = `gh workflow run release-controller.yml --repo ${DEFAULT_CANONICAL} -f mode=mirror -f version=${tag}`;
    } else {
      nextSafeCommand = "No release action is required.";
    }
  }

  return {
    current_state: currentState,
    blockers,
    next_safe_command: nextSafeCommand,
    safe_to_publish:
      blockers.length === 0 &&
      testpypi.published &&
      !pypi.published &&
      (github.tag_ref.exists || metadata.local_tag.exists),
  };
}

function humanSummary(result) {
  const lines = [
    "# Release State",
    "",
    `- Version: ${result.version}`,
    `- Tag: ${result.tag}`,
    `- Current state: ${result.current_state}`,
    `- Safe to publish: ${result.safe_to_publish ? "true" : "false"}`,
    `- Open PRs: ${result.open_pr_count ?? "unknown"}`,
    `- GitHub Release: ${result.github_release.exists ? (result.github_release.draft ? "draft" : "published") : "missing"}`,
    `- TestPyPI: ${result.testpypi.published ? "published" : "not published"}`,
    `- PyPI: ${result.pypi.published ? "published" : "not published"}`,
    `- Mirror main: ${result.mirror.main.status}`,
    `- Mirror tag ${result.tag}: ${result.mirror.tag.status}`,
    "",
    "## Blockers",
    ...(result.blockers.length > 0 ? result.blockers.map((item) => `- ${item}`) : ["- none"]),
    "",
    "## Next Safe Command",
    "",
    `\`${result.next_safe_command}\``,
  ];
  return `${lines.join("\n")}\n`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(usage());
    return;
  }

  splitRepo(args.repo);
  splitRepo(args.personal);
  const version = normalizeVersion(args.version);
  const tag = `v${version}`;
  const metadata = {
    versions: {
      "pyproject.toml": readPyprojectVersion(),
      "mcp.json": readJsonVersion("mcp.json"),
      "server.json": readJsonVersion("server.json"),
    },
    local_tag: localTagState(tag),
  };

  const [github, testpypi, pypi] = await Promise.all([
    inspectGitHub({ canonicalRepo: args.repo, tag, offline: args.offline }),
    args.offline ? Promise.resolve({ index: "TestPyPI", published: false, offline: true }) : pypiState("TestPyPI", version),
    args.offline ? Promise.resolve({ index: "PyPI", published: false, offline: true }) : pypiState("PyPI", version),
  ]);
  const mirror = inspectMirror({
    canonicalRepo: args.repo,
    personalRepo: args.personal,
    tag,
    offline: args.offline,
  });
  const decision = decideState({ github, testpypi, pypi, mirror, metadata, version, tag });

  const result = {
    current_state: decision.current_state,
    version,
    tag,
    open_pr_count: github.open_pr_count,
    open_prs: github.open_prs,
    closed_release_prs: github.closed_release_prs,
    metadata,
    git_tag: github.tag_ref,
    github_release: github.github_release,
    release_runs: github.release_runs,
    latest_release_run: github.release_runs[0] || null,
    testpypi,
    pypi,
    mirror: {
      ...mirror,
      latest_run: github.mirror_run,
    },
    blockers: decision.blockers,
    next_safe_command: decision.next_safe_command,
    safe_to_publish: decision.safe_to_publish,
  };

  const json = `${JSON.stringify(result, null, 2)}\n`;
  if (args.jsonOut) fs.writeFileSync(args.jsonOut, json, "utf8");
  process.stdout.write(args.json ? json : humanSummary(result));
}

main().catch((error) => {
  console.error(`release-state: ${error.message}`);
  process.exitCode = 2;
});
