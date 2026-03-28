#!/usr/bin/env python3
"""
Run all firmware tests in tests/firmware and write logs plus a summary into results/.
"""

from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
TEST_DIR = PROJECT_ROOT / "tests" / "firmware"
RESULTS_DIR = PROJECT_ROOT / "results"
RUNNER = PROJECT_ROOT / "run_firmware_test.py"
SRC_DIR = PROJECT_ROOT / "src"


def find_tests() -> list[Path]:
    return sorted(path for path in TEST_DIR.glob("*.asm"))


def run_one_test(asm_path: Path, results_dir: Path) -> dict[str, object]:
    expect_path = asm_path.with_suffix(".expect.json")
    if not expect_path.exists():
        raise FileNotFoundError(f"Expectation file not found for {asm_path.name}")

    cmd = [sys.executable, str(RUNNER), str(asm_path), str(expect_path)]
    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    log_path = results_dir / f"{asm_path.stem}.log"
    log_path.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    hex_path = results_dir / f"{asm_path.stem}.hex"
    vcd_path = results_dir / f"{asm_path.stem}.vcd"
    shutil.copy2(SRC_DIR / "memfile.hex", hex_path)
    if (SRC_DIR / "dump.vcd").exists():
        shutil.copy2(SRC_DIR / "dump.vcd", vcd_path)

    state_line = ""
    for line in proc.stdout.splitlines():
        if line.startswith("x0="):
            state_line = line.strip()
            break

    return {
        "name": asm_path.stem,
        "asm": asm_path.relative_to(PROJECT_ROOT).as_posix(),
        "expect": expect_path.relative_to(PROJECT_ROOT).as_posix(),
        "log": log_path.relative_to(PROJECT_ROOT).as_posix(),
        "hex": hex_path.relative_to(PROJECT_ROOT).as_posix(),
        "vcd": vcd_path.relative_to(PROJECT_ROOT).as_posix(),
        "returncode": proc.returncode,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "state_line": state_line,
    }


def write_summary(results_dir: Path, cases: list[dict[str, object]]) -> None:
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    passed = sum(1 for case in cases if case["status"] == "PASS")
    total = len(cases)

    summary_lines = [
        "# Firmware Suite Results",
        "",
        f"- Generated: {timestamp}",
        f"- Total tests: {total}",
        f"- Passed: {passed}",
        f"- Failed: {total - passed}",
        "",
        "## Test Cases",
        "",
        "| Test | Status | Assembly | Expectation | Log | HEX | VCD |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for case in cases:
        summary_lines.append(
            f"| {case['name']} | {case['status']} | `{case['asm']}` | "
            f"`{case['expect']}` | `{case['log']}` | `{case['hex']}` | `{case['vcd']}` |"
        )

    summary_lines.extend([
        "",
        "## Notes",
        "",
        "- Each `.log` file contains the full simulator console output for that test.",
        "- Each `.vcd` file is the waveform dump for that specific firmware test.",
        "- Each `.hex` file is the exact machine-code image loaded for that test.",
        "- Register expectations use architectural register names such as `x3`.",
        "- Memory expectations use word indices into `dmem.mem[]`, not byte addresses.",
        "",
        "## Simulation Snapshots",
        "",
    ])

    for case in cases:
        summary_lines.append(f"### {case['name']}")
        summary_lines.append("")
        summary_lines.append(f"- Status: {case['status']}")
        if case["state_line"]:
            summary_lines.append(f"- Final state: `{case['state_line']}`")
        summary_lines.append(f"- Log: `{case['log']}`")
        summary_lines.append(f"- HEX: `{case['hex']}`")
        summary_lines.append(f"- VCD: `{case['vcd']}`")
        summary_lines.append("")

    (results_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    (results_dir / "summary.json").write_text(json.dumps(cases, indent=2), encoding="utf-8")


def main() -> None:
    tests = find_tests()
    if not tests:
        raise SystemExit("No firmware tests found.")

    RESULTS_DIR.mkdir(exist_ok=True)
    latest_dir = RESULTS_DIR / "latest"
    latest_dir.mkdir(exist_ok=True)

    cases = []
    for asm_path in tests:
        case = run_one_test(asm_path, latest_dir)
        cases.append(case)
        print(f"{case['status']}: {case['name']}")

    write_summary(latest_dir, cases)

    failed = [case for case in cases if case["status"] != "PASS"]
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
