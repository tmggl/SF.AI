"""Phase 12 training gate.

The preflight can say PASS, but tokenizer training itself must remain blocked
until Sami explicitly approves Phase 12 and the command carries the confirmation
flag. These tests make that boundary executable.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from sf_ai.training.train_tokenizer import PHASE12_PERMISSION_ERROR, run


def test_train_tokenizer_refuses_without_phase12_confirmation(
    tmp_path: Path, capsys
) -> None:
    out_dir = tmp_path / "tokenizer"

    code = run(
        [
            "--corpus",
            "data/corpus/chat/jsonl",
            "--out",
            str(out_dir),
        ]
    )

    captured = capsys.readouterr()
    assert code == 2
    assert PHASE12_PERMISSION_ERROR in captured.err
    assert not out_dir.exists()


def test_train_bpe_script_refuses_without_phase12_confirmation(tmp_path: Path) -> None:
    out_dir = tmp_path / "tokenizer"

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/train_bpe.py",
            "--corpus",
            "data/corpus/chat/jsonl",
            "--out",
            str(out_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 2
    assert PHASE12_PERMISSION_ERROR in proc.stderr
    assert not out_dir.exists()
