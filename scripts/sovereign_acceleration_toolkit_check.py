#!/usr/bin/env python3
"""Verify the locally installed sovereign acceleration toolkit.

This is not a training step. It verifies engineering tools only: no pretrained
weights, no external model APIs, no external dialogue data.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata as metadata
import json
import platform
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/sovereign_acceleration_toolkit_report.json"
DEFAULT_DOC = ROOT / "docs/SOVEREIGN_ACCELERATION_TOOLKIT_LOADED.md"

REQUIRED_TOOLS = {
    "torch": "PyTorch compute engine",
    "numpy": "numeric arrays",
    "tensorboard": "local experiment visualization",
    "tqdm": "progress bars",
    "psutil": "local resource monitoring",
    "safetensors": "safe tensor serialization",
    "rich": "local CLI reports",
}

FORBIDDEN_SHORTCUTS = {
    "transformers": "common pretrained model loading path",
    "sentence_transformers": "pretrained embedding path",
    "openai": "hosted external AI API",
    "anthropic": "hosted external AI API",
    "google.generativeai": "hosted external AI API",
    "datasets": "external dataset hub path unless strictly isolated",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Verify SF.AI sovereign acceleration toolkit")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return p.parse_args()


def _version(package: str) -> str | None:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def _importable(module: str) -> bool:
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False


def _torch_info() -> dict[str, Any]:
    try:
        import torch
    except Exception as exc:
        return {"available": False, "error": str(exc)}
    return {
        "available": True,
        "version": getattr(torch, "__version__", "unknown"),
        "mps_available": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()),
        "cuda_available": bool(torch.cuda.is_available()),
        "amp_available": hasattr(torch, "autocast"),
    }


def _resource_info() -> dict[str, Any]:
    try:
        import psutil
    except Exception as exc:
        return {"available": False, "error": str(exc)}
    vm = psutil.virtual_memory()
    return {
        "available": True,
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "memory_total_gb": round(vm.total / (1024**3), 2),
        "memory_available_gb": round(vm.available / (1024**3), 2),
    }


def _write_doc(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Sovereign Acceleration Toolkit Loaded",
        "",
        "هذه ليست مرحلة تدريب، وليست تحميل أوزان أو بيانات خارجية. هذه حزمة",
        "أدوات هندسية محلية لتسريع SF.AI مع الحفاظ على السيادة.",
        "",
        f"- status: `{report['status']}`",
        f"- python: `{report['python']}`",
        f"- platform: `{report['platform']}`",
        f"- training_allowed: `{report['training_allowed']}`",
        f"- pretrained_weights_loaded: `{report['pretrained_weights_loaded']}`",
        f"- external_ai_api_used: `{report['external_ai_api_used']}`",
        "",
        "## الأدوات المحملة",
        "",
    ]
    for name, row in report["tools"].items():
        lines.append(f"- `{name}`: installed=`{row['installed']}`, version=`{row['version']}` — {row['purpose']}")
    lines.extend(
        [
            "",
            "## فحص الاختصارات الممنوعة",
            "",
        ]
    )
    for name, row in report["forbidden_shortcuts"].items():
        lines.append(f"- `{name}`: importable=`{row['importable']}` — {row['reason']}")
    lines.extend(
        [
            "",
            "## قرار الاستخدام",
            "",
            "- نستخدم هذه الأدوات للتتبع، التسريع، مراقبة الموارد، والتقارير.",
            "- لا نستخدمها لاستيراد عقل جاهز.",
            "- أي تدريب لاحق يبقى محجوبًا حتى تنجح Phase 27.80 gates.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    tools = {
        name: {
            "purpose": purpose,
            "installed": _importable(name),
            "version": _version(name.replace("_", "-")) or _version(name),
        }
        for name, purpose in REQUIRED_TOOLS.items()
    }
    forbidden = {
        name: {"reason": reason, "importable": _importable(name)}
        for name, reason in FORBIDDEN_SHORTCUTS.items()
    }
    missing = [name for name, row in tools.items() if not row["installed"]]
    risky = [name for name, row in forbidden.items() if row["importable"]]
    report = {
        "status": "READY" if not missing else "MISSING_TOOLS",
        "phase_context": "Phase 27.80 prerequisite — toolkit loadout, no training",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "training_allowed": False,
        "pretrained_weights_loaded": False,
        "external_ai_api_used": False,
        "external_dialogue_data_used": False,
        "tools": tools,
        "missing_tools": missing,
        "forbidden_shortcuts": forbidden,
        "risky_importable_shortcuts": risky,
        "torch": _torch_info(),
        "resources": _resource_info(),
        "next_step": "Phase 27.80 — encode repair gates and run dry-run validation",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _write_doc(args.doc, report)
    print("SF.AI — sovereign acceleration toolkit check")
    print(f"status: {report['status']}")
    print(f"missing_tools: {missing}")
    print(f"risky_importable_shortcuts: {risky}")
    print(f"report: {args.report.relative_to(ROOT)}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
