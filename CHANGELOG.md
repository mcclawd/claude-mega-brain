# Changelog

## v0.2.1 — 2026-06-30

### Added
- `scripts/okf_utils.py` — shared config, frontmatter, and path helpers
- `tests/test_okf.py` — unit tests for parse-okf, inject-links, and config

### Fixed
- `.mega-brain.json` `dir` field now limits the OKF scan root (was documented but not implemented)
- `inject-links.py` uses `CLAUDE_PROJECT_DIR` for relative paths (was `os.getcwd()`)
- Skills (`init`, `migrate`, `ingest`) aligned with flexible folder model — no hard `okf/` requirement
- `package.json` and plugin manifest versions aligned (`0.2.1`)

## v0.2.0 — 2026-06-29

### Added
- `.claude-plugin/plugin.json` — official plugin manifest with `name: mega-brain`, `displayName`, versioning
- `/mega-brain:init` skill — initializes OKF directory structure in any project
- `/mega-brain:migrate` skill — scans existing docs and generates OKF files
- `/mega-brain:ingest` skill — creates/updates individual OKF concept files
- `PostToolUse(Read)` hook — auto-surfaces linked concepts when navigating OKF files
- `.mega-brain.json` project config — override dir, maxConcepts, priorityTypes
- `log.md` support — last 3 changelog entries injected at session start
- Body excerpt fallback — uses first sentence from file body if `description` missing
- Agentic benchmark — real `claude -p` sessions vs Obsidian+MCP

### Changed
- Plugin renamed from `claude-lore` → `mega-brain` (skill namespace)
- Context tag renamed `<lore>` → `<mega-brain>`
- Config file renamed `.lore.json` → `.mega-brain.json`
- Hook uses `CLAUDE_PROJECT_DIR` env var (official, with PWD fallback)

## v0.1.0 — 2026-06-29

### Added
- Initial release
- `SessionStart` hook — injects OKF index at session start
- `parse-okf.py` — YAML frontmatter parser
- `scripts/inject-links.py` — PostToolUse link injector
- `skills/claude-mega-brain` — OKF navigation skill
- Benchmark suite with promptfoo
