from __future__ import annotations

import importlib
import json

REQUIRED_MODULES = ["fitz", "pydantic", "openai", "pandas", "PySide6"]


def run_doctor() -> dict[str, str]:
    status: dict[str, str] = {}
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
            status[module] = "ok"
        except Exception as exc:  # noqa: BLE001
            status[module] = f"error: {exc}"
    return status


def main() -> int:
    print(json.dumps(run_doctor(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
