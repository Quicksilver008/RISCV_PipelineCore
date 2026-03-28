#!/usr/bin/env python3
"""
Assemble a firmware test, generate simulation checks, compile the RTL, and run it.

Usage:
    python run_firmware_test.py sample_program.asm tests/firmware/sample_program.expect.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, Tuple

from riscv_assembler import RISC_V_Assembler


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
HEX_FILE = SRC_DIR / "memfile.hex"
TB_FILE = SRC_DIR / "pipeline_tb.v"
OUT_FILE = SRC_DIR / "out_check.vvp"
CONFIG_FILE = SRC_DIR / "test_config.vh"
CHECKS_FILE = SRC_DIR / "test_checks.vh"


def parse_value(value: object) -> int:
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        raise ValueError(f"Unsupported expectation value: {value!r}")
    value = value.strip().lower()
    if value.startswith("0x"):
        return int(value, 16)
    if value.startswith("0b"):
        return int(value, 2)
    return int(value, 10)


def reg_index(name: str) -> int:
    name = name.strip().lower()
    if not name.startswith("x"):
        raise ValueError(f"Register name must be xN, got {name!r}")
    index = int(name[1:])
    if index < 0 or index > 31:
        raise ValueError(f"Register out of range: {name}")
    return index


def build_checks(expectations: Dict[str, object]) -> Tuple[str, str]:
    name = str(expectations.get("name", "firmware_test"))
    cycles = int(expectations.get("cycles", 20))
    checks = []

    registers = expectations.get("registers", {})
    if not isinstance(registers, dict):
        raise ValueError("'registers' must be an object")
    for reg_name, reg_value in sorted(registers.items(), key=lambda item: reg_index(item[0])):
        idx = reg_index(reg_name)
        value = parse_value(reg_value) & 0xFFFFFFFF
        checks.append(
            f'        if (dut.Decode.rf.registers[{idx}] !== 32\'h{value:08x}) '
            f'$fatal(1, "{reg_name} mismatch");'
        )

    memory = expectations.get("memory", {})
    if not isinstance(memory, dict):
        raise ValueError("'memory' must be an object")
    for addr_name, mem_value in sorted(memory.items(), key=lambda item: int(item[0])):
        addr = int(addr_name)
        if addr < 0:
            raise ValueError(f"Memory address must be non-negative, got {addr}")
        value = parse_value(mem_value) & 0xFFFFFFFF
        checks.append(
            f'        if (dut.Memory.dmem.mem[{addr}] !== 32\'h{value:08x}) '
            f'$fatal(1, "memory[{addr}] mismatch");'
        )

    checks.append(f'        $display("Firmware test {name} passed.");')
    config_text = f"`ifndef TEST_CYCLES\n`define TEST_CYCLES {cycles}\n`endif\n"
    checks_text = "\n".join(checks) + "\n"
    return config_text, checks_text


def run_command(cmd: Iterable[str], cwd: Path) -> None:
    process = subprocess.run(list(cmd), cwd=cwd, check=False)
    if process.returncode != 0:
        raise SystemExit(process.returncode)


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Usage: python run_firmware_test.py <program.asm> [expect.json]")
        raise SystemExit(1)

    asm_path = Path(sys.argv[1]).resolve()
    if not asm_path.exists():
        raise FileNotFoundError(f"Assembly file not found: {asm_path}")

    if len(sys.argv) == 3:
        expect_path = Path(sys.argv[2]).resolve()
    else:
        expect_path = asm_path.with_suffix(".expect.json")
    if not expect_path.exists():
        raise FileNotFoundError(f"Expectation file not found: {expect_path}")

    assembler = RISC_V_Assembler()
    assembler.assemble_file(str(asm_path), str(HEX_FILE))
    sys.stdout.flush()

    expectations = json.loads(expect_path.read_text())
    config_text, checks_text = build_checks(expectations)
    CONFIG_FILE.write_text(config_text, encoding="ascii")
    CHECKS_FILE.write_text(checks_text, encoding="ascii")

    print(f"Compiled expectations from {expect_path.name}")
    sys.stdout.flush()
    run_command(["iverilog", "-o", str(OUT_FILE), str(TB_FILE)], SRC_DIR)
    run_command(["vvp", str(OUT_FILE)], SRC_DIR)


if __name__ == "__main__":
    main()
