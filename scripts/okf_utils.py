"""Shared helpers for claude-mega-brain OKF scripts."""
import json
import os
import re

SKIP_DIRS = {
    'node_modules', '.git', '.cache', 'vendor', 'dist', 'build',
    '__pycache__', '.venv', 'venv', '.tox', 'coverage', '.nyc_output',
    'target', '.gradle', 'Pods', '.dart_tool', '.flutter-plugins',
}


def get_project_root():
    return os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()


def load_config(project_root):
    try:
        with open(os.path.join(project_root, '.mega-brain.json'), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def get_scan_root(project_root, cfg=None):
    """Return the directory to walk when scanning for OKF concepts."""
    if cfg is None:
        cfg = load_config(project_root)
    subdir = cfg.get('dir', '').strip()
    if not subdir:
        return project_root
    scan_root = os.path.realpath(os.path.join(project_root, subdir))
    project_real = os.path.realpath(project_root)
    if not scan_root.startswith(project_real + os.sep) and scan_root != project_real:
        return project_root
    if not os.path.isdir(scan_root):
        return project_root
    return scan_root


def parse_frontmatter(content):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?', content, re.DOTALL)
    if not m:
        return {}, 0
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('"\'')
    return fm, m.end()


def is_okf_concept(fm, fname):
    return bool(fm.get('type')) or fname == 'index.md'
