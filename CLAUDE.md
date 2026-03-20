# CLAUDE.md

This repository is the GitHub-backed content repo for the Apache Pinot docs site. Treat it as a documentation product, not as a generic Markdown repo.

## What This Repo Is

- The docs site is powered by GitBook.
- The docs entrypoints are defined in `.gitbook.yaml`:
  - `README.md` is the root landing page.
  - `SUMMARY.md` is the navigation tree.
- Many pages use GitBook-specific markup such as `content-ref`, `hint`, `figure`, and frontmatter blocks. Preserve that syntax unless there is a clear reason to change it.
- The default PR base branch is `latest`.

## Primary Source Of Truth

- For product behavior, APIs, config keys, planner rules, minion tasks, query options, and function names, the source of truth is the Apache Pinot source repo, not memory and not old docs text.
- Cross-check facts against a local clone of `apache/pinot` whenever the docs describe shipped behavior.
- If a local clone is not available, use `gh repo clone apache/pinot ../apache-pinot` or another nearby path.
- Prefer inspecting code, constants, tests, and integration tests over guessing.

## Repo-Specific Editing Rules

- Keep the docs task-oriented. Favor user journeys such as:
  - overview
  - get started
  - ingest and model data
  - query and build applications
  - operate Pinot
  - develop and extend Pinot
  - reference
- When changing information architecture, update all three together when needed:
  - `README.md`
  - `SUMMARY.md`
  - the relevant landing pages for the affected section
- Every page should be discoverable from either `SUMMARY.md` or a landing page. Hidden pages are usually a docs bug.
- Do not move or rename files casually. Existing docs URLs may be linked from blog posts, issues, release notes, or the main Pinot repo.
- If you must change a path, add or update redirects in `.gitbook.yaml` and update internal links in the same change.
- Prefer adding navigation and landing-page links before doing large file moves.
- Preserve frontmatter and page titles unless there is a strong reason to change them.
- Use relative links or GitBook `content-ref` blocks for internal navigation. Avoid hardcoding GitHub blob URLs when an internal docs link will work.

## Known Structural Risks

- Function documentation is split across multiple surfaces:
  - `functions/`
  - `functions-1/`
  - `configuration-reference/functions/`
- Avoid creating a fourth surface. Prefer improving discoverability and pointing to a canonical page.
- Top-level docs changes can easily drift into broken navigation if `SUMMARY.md` is not kept in sync.
- Some pages may exist only because of legacy URLs. Before deleting anything, check whether a redirect would be safer.

## Style

- Follow `contributing/style-guide.md`.
- Follow the Google developer documentation style guide for anything not covered locally.
- Pinot-specific wording rule already documented here:
  - use `star-tree` as an adjective
  - use `star tree` as a noun
- Prefer concrete, source-backed statements over marketing language.
- Call out version caveats explicitly when behavior differs by Pinot release.

## Validation Expectations

There is no obvious local site build command in this repo, so validation is mostly structural and factual.

Always run:

```bash
git diff --check
```

When editing links or navigation, also validate that changed links resolve. A lightweight approach is fine, for example checking edited files for `content-ref` targets and relative Markdown links.

When editing facts about Pinot behavior, also validate against source:

- planner rules: query planner constants and tests
- minion tasks: task generator/executor classes and integration tests
- query options: constants and request handling code
- function names/signatures: function classes, enums, and tests

## Git And GitHub Workflow

- Use `gh` for GitHub operations.
- Base PRs against `latest` unless the repo state clearly requires otherwise.
- Keep commits clean and purposeful.
- The repo owner prefers avoiding a pile of incremental commits. If you are asked to commit repeatedly during the same task, prefer amending the in-progress commit instead of stacking noise.
- In PR descriptions, explain:
  - what changed for readers
  - what was structurally reorganized
  - what was cross-checked against `apache/pinot`
  - how you validated the change

## Good Default Workflow

1. Read `README.md`, `SUMMARY.md`, `.gitbook.yaml`, and the relevant landing pages.
2. If the change describes Pinot behavior, inspect the corresponding code in `apache/pinot`.
3. Make the smallest change that improves discoverability and correctness.
4. Update navigation and landing pages together when the change affects how users find content.
5. Run structural validation and source cross-checks.
6. Open or update a PR against `latest` with a concise explanation of the user-facing impact.
