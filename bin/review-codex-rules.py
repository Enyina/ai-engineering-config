#!/usr/bin/env python3
"""Review local Codex prefix approvals without echoing commands or uploading files.

This is a conservative heuristic inventory, not a parser for every Codex rule
syntax or a replacement for the effective security/approval policy.
"""
import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path

ENTRY = re.compile(r'\bprefix_rule\s*\(\s*pattern\s*=\s*\[\s*"([^"\\]+)"(?:\s*,\s*"([^"\\]+)")?', re.I)
DECISION = re.compile(r'\bdecision\s*=\s*"([^"]+)"')
SENSITIVE = re.compile(r'prisma|database_url|auth.storage|\bpatient\b|\bpatients\b|\border\b|\borders\b|pharmacy|dispensary|prescri|\bjwt\b|access.token|api.key|token|/tmp/[^\s"\\]+\.py|localhost:\d+|coresimulator', re.I)
READ = {('git','status'),('git','log'),('git','diff'),('git','rev-parse'),('rg','--files'),('rg','-n'),('sed','-n'),('docker','ps'),('lsof','')}
BLOCK_GIT = {'add','commit','restore','push','merge','cherry-pick','switch','worktree','rm','pull','reset','rebase'}
RISK = {'rm','kill','pkill','node','/bin/zsh','bash','sh','python','python3','curl'}
CATEGORY_ORDER = ('project_or_sensitive', 'high_impact', 'read_oriented', 'task_specific', 'unrecognized')

def group(line):
    match = ENTRY.search(line)
    if not match:
        return 'unrecognized'
    first, second = match.group(1), match.group(2) or ''
    if SENSITIVE.search(line):
        return 'project_or_sensitive'
    if first in RISK or (first == 'git' and second in BLOCK_GIT) or (first == 'docker' and second in {'build','run','exec'}):
        return 'high_impact'
    if (first,second) in READ:
        return 'read_oriented'
    return 'task_specific'

def audit(source):
    counts = Counter()
    decisions = Counter()
    unparsed = 0
    for line in source.splitlines():
        if 'prefix_rule(' not in line:
            continue
        counts[group(line)] += 1
        d = DECISION.search(line)
        decisions[d.group(1) if d else 'unknown'] += 1
        if not ENTRY.search(line):
            unparsed += 1
    return {
        'total_rules': sum(counts.values()),
        'decisions': dict(decisions),
        'categories': {key: counts[key] for key in CATEGORY_ORDER},
        'unparsed': unparsed,
        'advice': [
            'Do not commit the raw rules file or snapshot into a personal repository.',
            'Exclude project-specific and potentially confidential commands from portable rules.',
            'Remove broad automatic approvals for write-capable, destructive and shell-evaluation commands.',
            'Review read-oriented candidates before enabling a narrow personal allowlist.',
            'Keep command permissions separate from engineering instructions.'
        ]
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default=str(Path(os.getenv('CODEX_HOME', Path.home()/'.codex'))/'rules'/'default.rules'),
                        help='Local Codex rules file; never uploaded.')
    parser.add_argument('--json', action='store_true', help='Sanitized output without commands or paths.')
    args = parser.parse_args()
    try:
        report = audit(Path(args.input).read_text(encoding='utf-8'))
    except (OSError, UnicodeError):
        parser.error('Cannot read the requested local rules file.')
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print('Codex command permission review (local-only; no changes)')
    print('Rules:', report['total_rules'])
    print('Decisions:', ', '.join(k+'='+str(v) for k,v in report['decisions'].items()))
    for key, count in report['categories'].items():
        print('  '+key+': '+str(count))
    if report['unparsed']:
        print('WARNING: entries not recognized; manual review still required.')
    for advice in report['advice']:
        print('- '+advice)
    print('No changes or uploads were made.')

if __name__ == '__main__':
    main()
