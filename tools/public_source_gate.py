#!/usr/bin/env python3
"""Fail closed on unverified public Flip the Tables source before debug CI.

This test does not import or request private application code and never changes
files. It recognizes a staged export only when the export's SHA-256 manifest is
present, checks every manifest entry byte-for-byte, and rejects extra source
or private artifacts. Human rights/provenance approval remains separate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

BANNED_SUFFIXES = {'.pdf', '.apk', '.aab', '.jks', '.keystore', '.p12', '.pem', '.key', '.env', '.jpg', '.jpeg'}
BANNED_PARTS = {'.git', 'private', '__pycache__', 'build', 'outputs', 'screenshots', 'downloads'}
REQUIRED = {
    'VERSION.txt', 'EDITION.txt', 'web/index.html', 'web/app.js',
    'web/private-library.js', 'web/versions.js', 'web/version.txt',
    'android/app/build.gradle', 'android/app/src/main/AndroidManifest.xml',
    '.github/workflows/public-android.yml',
    *{f'web/public-domain-web/part-{n:02d}.json' for n in range(1, 7)},
}
EXTRA_PUBLIC_PATHS = {
    'PUBLIC_EXPORT_SHA256.json', '.gitignore', 'README.md',
    'docs/QUIET_STARTUP_NOTE.md', 'docs/FUTURE_PHASE_FRAMEWORK.md',
    '.github/workflows/public-safety.yml',
    'tools/public_source_gate.py', 'tests/test_public_source_gate.py',
}

class GateError(ValueError):
    pass


def validate(root: Path) -> int:
    source = root / 'PUBLIC_EXPORT_SHA256.json'
    if not source.is_file() or source.is_symlink():
        raise GateError('No verified public export manifest; Android build NOT authorized')
    try:
        doc = json.loads(source.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise GateError('Invalid public export manifest') from exc
    if not isinstance(doc, dict) or doc.get('schema') != 1 or not isinstance(doc.get('files'), dict):
        raise GateError('Public export manifest schema mismatch')
    entries = doc['files']
    if not REQUIRED.issubset(entries):
        raise GateError('Public export missing required Android / WEB files')
    if len(entries) < 70:
        raise GateError('Truncated public export inventory')
    for raw_path, digest in entries.items():
        if not isinstance(raw_path, str) or not isinstance(digest, str):
            raise GateError('Invalid export inventory entry')
        path = PurePosixPath(raw_path)
        if path.is_absolute() or any(p in ('..', '.') or p in BANNED_PARTS for p in path.parts):
            raise GateError(f'Unsafe export path: {raw_path}')
        if path.suffix.lower() in BANNED_SUFFIXES:
            raise GateError(f'Forbidden artifact in source: {raw_path}')
        if len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise GateError(f'Invalid SHA-256 digest: {raw_path}')
        candidate = root.joinpath(*path.parts)
        if not candidate.is_file() or candidate.is_symlink():
            raise GateError(f'Missing or symlinked export: {raw_path}')
        actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if actual != digest:
            raise GateError(f'Export checksum mismatch: {raw_path}')

    for item in root.rglob('*'):
        if '.git' in item.parts or '__pycache__' in item.parts:
            continue
        if not item.is_file():
            continue
        relative = item.relative_to(root).as_posix()
        if item.is_symlink():
            raise GateError(f'Unexpected symlink: {relative}')
        if any(p in BANNED_PARTS for p in PurePosixPath(relative).parts):
            raise GateError(f'Private/generated directory: {relative}')
        if item.suffix.lower() in BANNED_SUFFIXES:
            raise GateError(f'Forbidden public file: {relative}')
        if relative not in entries and relative not in EXTRA_PUBLIC_PATHS:
            raise GateError(f'Unexpected file outside reviewed export: {relative}')

    if (root / 'EDITION.txt').read_text(encoding='utf-8').strip() != 'public':
        raise GateError('Public edition marker missing')
    if (root / 'web/private-library.js').read_text(encoding='utf-8').strip() != 'window.FTT_PRIVATE_PACKS = [];':
        raise GateError('Private Bible descriptor must stay empty')
    if (root / 'VERSION.txt').read_bytes().strip() != (root / 'web/version.txt').read_bytes().strip():
        raise GateError('Public version mismatch')
    gradle = (root / 'android/app/build.gradle').read_text(encoding='utf-8')
    if 'permanentUpgrade' in gradle or 'justinOnly' in gradle or 'FTT_SIGNING' in gradle:
        raise GateError('Private upgrade flavor or permanent signing found in public Gradle')
    ci = (root / '.github/workflows/public-android.yml').read_text(encoding='utf-8')
    if 'assemblePublicReleaseDebug' not in ci or 'NOT-FOR-UPGRADES' not in ci:
        raise GateError('Public CI must only distribute explicitly labeled debug artifacts')
    if 'assembleJustinOnly' in ci or 'FTT_SIGNING' in ci or 'self-hosted' in ci:
        raise GateError('Public CI contains private signing or nonstandard runner')
    return len(entries)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    try:
        files = validate(a.root.resolve())
    except (OSError, GateError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 1
    print(f'PASS: {files} checksum-verified public source files; eligible for public debug CI only')
    print('NOTE: passing checksums does NOT replace a human copyright/artwork audit')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
