#!/usr/bin/env python3
"""Scan project for OKF concepts (any .md with type: frontmatter) and print a compact index."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_utils import SKIP_DIRS, get_scan_root, is_okf_concept, load_config, parse_frontmatter


def body_excerpt(content, fm_end):
    body = content[fm_end:].strip()
    body = re.sub(r'^#+[^\n]+\n', '', body, flags=re.MULTILINE).strip()
    body = re.sub(r'^\|.+', '', body, flags=re.MULTILINE).strip()
    m = re.match(r'([^.\n!?]{10,}[.!?])', body)
    if m:
        return m.group(1).strip()[:100]
    first = body.split('\n')[0].strip()
    return first[:100] if len(first) > 10 else ''


def last_log_entries(log_path, n=3):
    try:
        with open(log_path, encoding='utf-8', errors='replace') as f:
            content = f.read()
        m = re.match(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
        body = content[m.end():] if m else content
        lines = [l.strip() for l in body.splitlines() if l.strip() and not l.startswith('#')]
        return lines[-n:]
    except OSError:
        return []


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    project_root = os.path.realpath(sys.argv[1])
    cfg = load_config(project_root)
    scan_root = get_scan_root(project_root, cfg)
    max_concepts = int(cfg.get('maxConcepts', 60))
    priority_types = cfg.get('priorityTypes', [])
    extra_skip = set(cfg.get('exclude', []))
    skip = SKIP_DIRS | extra_skip

    concepts = []
    log_entries = []

    for root, dirs, files in os.walk(scan_root):
        dirs[:] = sorted(d for d in dirs if d not in skip and not d.startswith('.cache'))

        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, project_root)

            if fname == 'log.md' and not log_entries:
                log_entries = last_log_entries(fpath)
                continue

            try:
                with open(fpath, encoding='utf-8', errors='replace') as f:
                    content = f.read(4000)
                fm, fm_end = parse_frontmatter(content)
                if not is_okf_concept(fm, fname):
                    continue
                desc = fm.get('description', '') or body_excerpt(content, fm_end)
                concept_type = fm.get('type', '')
                concepts.append({
                    'path': rel,
                    'type': concept_type,
                    'desc': desc[:100],
                    'is_index': fname == 'index.md',
                    'priority': priority_types.index(concept_type) if concept_type in priority_types else 999,
                })
            except OSError:
                pass

    concepts.sort(key=lambda c: (0 if c['is_index'] else 1, c['priority'], c['path']))

    count = len(concepts)
    lines = [
        f"Knowledge: {count} documented concept{'s' if count != 1 else ''} found in project",
        "Concepts with `type:` frontmatter — read any file for full details.",
    ]

    if log_entries:
        lines += ["", "Recent (log.md):"] + [f"  {e}" for e in log_entries]

    lines.append("")
    for c in concepts[:max_concepts]:
        typ = f" [{c['type']}]" if c['type'] else ''
        desc = f" — {c['desc']}" if c['desc'] else ''
        lines.append(f"  {c['path']}{typ}{desc}")

    if count > max_concepts:
        lines.append(f"  ... +{count - max_concepts} more")

    print('\n'.join(lines))


if __name__ == '__main__':
    main()
