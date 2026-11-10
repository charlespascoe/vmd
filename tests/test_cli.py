"""CLI regression tests: unreadable input files must fail cleanly."""
import sys

import pytest

from vmd import main


def test_missing_file_reports_clean_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['vmd', 'does-not-exist-xyz.md'])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert 'does-not-exist-xyz.md' in err
    assert 'Traceback' not in err


def test_undecodable_file_reports_clean_error(monkeypatch, capsys, tmp_path):
    bad = tmp_path / 'bad.md'
    bad.write_bytes(b'# title \x81 broken\n')
    monkeypatch.setattr(sys, 'argv', ['vmd', str(bad)])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert 'bad.md' in err
    assert 'Traceback' not in err
