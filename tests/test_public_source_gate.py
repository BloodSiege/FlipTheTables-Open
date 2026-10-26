#!/usr/bin/env python3
"""Offline synthetic regression tests for the public source checksum gate.

Creates only temporary, invented files. Never reads private app sources, signing
credentials, personal Bibles, or a real public staging export.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

GATE_PATH = Path(__file__).resolve().parents[1] / 'tools' / 'public_source_gate.py'
spec = importlib.util.spec_from_file_location('ftt_public_source_gate', GATE_PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class PublicSourceGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ftt-gate-synthetic-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'staging'
        self.root.mkdir()
        self.contents = {name: b'fixture' for name in gate.REQUIRED}
        self.contents.update({
            'VERSION.txt': b'0.0.0\n',
            'web/version.txt': b'0.0.0\n',
            'EDITION.txt': b'public\n',
            'web/private-library.js': b'window.FTT_PRIVATE_PACKS = [];\n',
            'android/app/build.gradle': b'// public debug fixture\n',
            '.github/workflows/public-android.yml':
                b'assemblePublicReleaseDebug\nNOT-FOR-UPGRADES\n',
        })
        for i in range(70 - len(self.contents)):
            self.contents[f'web/backgrounds/fixture-{i:03}.svg'] = b'<svg/>\n'
        self._write_fixture()

    def _write_fixture(self):
        for name, value in self.contents.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        self._manifest()

    def _manifest(self):
        checksums = {
            name: hashlib.sha256(data).hexdigest()
            for name, data in sorted(self.contents.items())
        }
        (self.root / 'PUBLIC_EXPORT_SHA256.json').write_text(
            json.dumps({'schema': 1, 'files': checksums}), encoding='utf-8')

    def test_valid_synthetic_export(self):
        self.assertEqual(gate.validate(self.root), 70)

    def test_missing_manifest_blocks(self):
        (self.root / 'PUBLIC_EXPORT_SHA256.json').unlink()
        with self.assertRaises(gate.GateError):
            gate.validate(self.root)

    def test_modified_source_blocks(self):
        (self.root / 'web/app.js').write_bytes(b'tampered')
        with self.assertRaisesRegex(gate.GateError, 'checksum mismatch'):
            gate.validate(self.root)

    def test_unmanifested_source_blocks(self):
        (self.root / 'web/extra.js').write_text('extra', encoding='utf-8')
        with self.assertRaisesRegex(gate.GateError, 'Unexpected file'):
            gate.validate(self.root)

    def test_private_directory_blocks(self):
        path = self.root / 'web/private/secret.json'
        path.parent.mkdir(parents=True)
        path.write_text('synthetic', encoding='utf-8')
        with self.assertRaisesRegex(gate.GateError, 'Private/generated directory'):
            gate.validate(self.root)

    def test_symlinked_source_ancestor_blocks(self):
        with tempfile.TemporaryDirectory(prefix='ftt-gate-outside-') as outside:
            background_dir = self.root / 'web/backgrounds'
            moved = Path(outside) / 'backgrounds'
            background_dir.rename(moved)
            background_dir.symlink_to(moved, target_is_directory=True)
            with self.assertRaises(gate.GateError):
                gate.validate(self.root)

    def test_symlinked_manifest_blocks(self):
        manifest = self.root / 'PUBLIC_EXPORT_SHA256.json'
        original = self.root / 'manifest-copy.json'
        manifest.rename(original)
        manifest.symlink_to(original)
        with self.assertRaises(gate.GateError):
            gate.validate(self.root)

    def test_repeated_separator_manifest_alias_blocks(self):
        # An alias of an already-counted file must not pad the manifest count.
        self.contents['web//app.js'] = self.contents['web/app.js']
        self._manifest()
        with self.assertRaisesRegex(gate.GateError, 'Noncanonical export path'):
            gate.validate(self.root)

    def test_dot_component_manifest_alias_blocks(self):
        self.contents['web/./app.js'] = self.contents['web/app.js']
        self._manifest()
        with self.assertRaisesRegex(gate.GateError, 'Noncanonical export path'):
            gate.validate(self.root)

    def test_backslash_manifest_path_blocks(self):
        # A backslash is a filename character on Linux, not a separator.
        self.contents['web\\shadow.js'] = b'fixture'
        self._write_fixture()
        with self.assertRaisesRegex(gate.GateError, 'Noncanonical export path'):
            gate.validate(self.root)

    def test_private_library_descriptor_blocks_even_when_rehashed(self):
        self.contents['web/private-library.js'] = b'window.FTT_PRIVATE_PACKS = ["synthetic"];\n'
        self._write_fixture()
        with self.assertRaisesRegex(gate.GateError, 'Private Bible descriptor'):
            gate.validate(self.root)

    def test_private_signing_marker_blocks_even_when_rehashed(self):
        self.contents['android/app/build.gradle'] = b'// FTT_SIGNING\n'
        self._write_fixture()
        with self.assertRaisesRegex(gate.GateError, 'Private upgrade flavor'):
            gate.validate(self.root)

    def test_missing_required_file_blocks(self):
        self.contents.pop('web/index.html')
        (self.root / 'web/index.html').unlink()
        self._manifest()
        with self.assertRaisesRegex(gate.GateError, 'missing required'):
            gate.validate(self.root)

    def test_mismatched_versions_block_even_when_rehashed(self):
        self.contents['web/version.txt'] = b'9.9.9\n'
        self._write_fixture()
        with self.assertRaisesRegex(gate.GateError, 'version mismatch'):
            gate.validate(self.root)

    def test_private_ci_marker_blocks_even_when_rehashed(self):
        self.contents['.github/workflows/public-android.yml'] += b'FTT_SIGNING\n'
        self._write_fixture()
        with self.assertRaisesRegex(gate.GateError, 'private signing'):
            gate.validate(self.root)


if __name__ == '__main__':
    unittest.main()
