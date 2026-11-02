#!/usr/bin/env python3
"""Validate skill format, portable references, metadata, and evaluation inputs."""
from pathlib import Path
import ast
import json
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml
from skills_ref.validator import validate

ROOT = Path(__file__).resolve().parents[1]


def check_links(path, boundary):
    errors = []
    # Markdown inline and reference-style link destinations; external URLs are
    # intentionally not fetched by an offline package-integrity check.
    text = path.read_text()
    destinations = re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
    destinations += re.findall(r'^\[[^\]]+\]:\s*(\S+)', text, re.M)
    for target in destinations:
        target = target.strip('<>')
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith('#'):
            continue
        local = unquote(parsed.path)
        resolved = (path.parent / local).resolve()
        if not resolved.is_relative_to(boundary):
            errors.append(f'{path.relative_to(ROOT)}: reference escapes package: {target}')
        elif not resolved.exists():
            errors.append(f'{path.relative_to(ROOT)}: missing reference: {target}')
    return errors


def main():
    errors = []
    skills = sorted((ROOT / 'skills').iterdir())
    for skill in skills:
        if not skill.is_dir():
            continue
        errors += [f'{skill.name}: {error}' for error in validate(skill)]
        entry = (skill / 'SKILL.md').read_text()
        if len(entry.splitlines()) >= 500:
            errors.append(f'{skill.name}: entry point should stay below 500 lines')
        metadata = yaml.safe_load(entry.split('---', 2)[1])
        if metadata.get('license') != 'MIT' or not (skill / 'LICENSE').is_file():
            errors.append(f'{skill.name}: missing portable license')
        extras = metadata.get('metadata', {})
        if not isinstance(extras, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in extras.items()):
            errors.append(f'{skill.name}: metadata must contain string keys and values')
        ui = yaml.safe_load((skill / 'agents/openai.yaml').read_text())['interface']
        if not 25 <= len(ui['short_description']) <= 64:
            errors.append(f'{skill.name}: short description must be 25-64 characters')
        if '$' + skill.name not in ui['default_prompt']:
            errors.append(f'{skill.name}: prompt must name its skill')
        queries = json.loads((skill / 'evals/triggers.json').read_text())['queries']
        if not all(isinstance(q.get('query'), str) and type(q.get('should_trigger')) is bool for q in queries):
            errors.append(f'{skill.name}: malformed activation cases')
        if {q['should_trigger'] for q in queries} != {True, False}:
            errors.append(f'{skill.name}: activation cases need positive and negative examples')
        for path in skill.rglob('*'):
            if path.is_symlink():
                errors.append(f'{path}: symlinks are not portable package content')
            if path.suffix == '.md':
                errors += check_links(path, skill)
                if re.search(r'/Users/|/home/|docs/research/hmi-handbook', path.read_text()):
                    errors.append(f'{path.relative_to(ROOT)}: workstation/private research reference')
            if path.suffix == '.py':
                ast.parse(path.read_text(), filename=str(path))
        print(f'Checked {skill.name}')
    for path in [*ROOT.glob('*.md'), *(ROOT / 'docs').glob('*.md')]:
        errors += check_links(path, ROOT)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('PASS: official format, local file links, metadata, licenses, and evaluation inputs')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
