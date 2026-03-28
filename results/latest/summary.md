# Firmware Suite Results

- Generated: 2026-03-28 17:00:39
- Total tests: 5
- Passed: 5
- Failed: 0

## Test Cases

| Test | Status | Assembly | Expectation | Log | HEX | VCD |
| --- | --- | --- | --- | --- | --- | --- |
| alu_all | PASS | `tests/firmware/alu_all.asm` | `tests/firmware/alu_all.expect.json` | `results/latest/alu_all.log` | `results/latest/alu_all.hex` | `results/latest/alu_all.vcd` |
| branch_logic | PASS | `tests/firmware/branch_logic.asm` | `tests/firmware/branch_logic.expect.json` | `results/latest/branch_logic.log` | `results/latest/branch_logic.hex` | `results/latest/branch_logic.vcd` |
| jump_ops | PASS | `tests/firmware/jump_ops.asm` | `tests/firmware/jump_ops.expect.json` | `results/latest/jump_ops.log` | `results/latest/jump_ops.hex` | `results/latest/jump_ops.vcd` |
| memory_hazard | PASS | `tests/firmware/memory_hazard.asm` | `tests/firmware/memory_hazard.expect.json` | `results/latest/memory_hazard.log` | `results/latest/memory_hazard.hex` | `results/latest/memory_hazard.vcd` |
| shift_ops | PASS | `tests/firmware/shift_ops.asm` | `tests/firmware/shift_ops.expect.json` | `results/latest/shift_ops.log` | `results/latest/shift_ops.hex` | `results/latest/shift_ops.vcd` |

## Notes

- Each `.log` file contains the full simulator console output for that test.
- Each `.vcd` file is the waveform dump for that specific firmware test.
- Each `.hex` file is the exact machine-code image loaded for that test.
- Register expectations use architectural register names such as `x3`.
- Memory expectations use word indices into `dmem.mem[]`, not byte addresses.

## Simulation Snapshots

### alu_all

- Status: PASS
- Final state: `x0=00000000 x1=00000005 x2=00000009 x3=0000000e x4=00000004 x5=00000008 x6=00000005 x7=00000001 x8=00000000 x9=00000000 x10=00000000 x11=00000000 mem0=00000000`
- Log: `results/latest/alu_all.log`
- HEX: `results/latest/alu_all.hex`
- VCD: `results/latest/alu_all.vcd`

### branch_logic

- Status: PASS
- Final state: `x0=00000000 x1=00000001 x2=00000001 x3=00000007 x4=00000002 x5=00000007 x6=00000002 x7=00000001 x8=0000000b x9=00000004 x10=00000000 x11=00000000 mem0=00000000`
- Log: `results/latest/branch_logic.log`
- HEX: `results/latest/branch_logic.hex`
- VCD: `results/latest/branch_logic.vcd`

### jump_ops

- Status: PASS
- Final state: `x0=00000000 x1=00000004 x2=00000007 x3=00000014 x4=00000009 x5=00000008 x6=00000018 x7=00000000 x8=00000000 x9=00000000 x10=00000000 x11=00000000 mem0=00000000`
- Log: `results/latest/jump_ops.log`
- HEX: `results/latest/jump_ops.hex`
- VCD: `results/latest/jump_ops.vcd`

### memory_hazard

- Status: PASS
- Final state: `x0=00000000 x1=0000000c x2=00000003 x3=0000000c x4=0000000f x5=0000000f x6=0000000c x7=00000000 x8=00000000 x9=00000000 x10=00000000 x11=00000000 mem0=0000000c`
- Log: `results/latest/memory_hazard.log`
- HEX: `results/latest/memory_hazard.hex`
- VCD: `results/latest/memory_hazard.vcd`

### shift_ops

- Status: PASS
- Final state: `x0=00000000 x1=00000001 x2=00000008 x3=00000001 x4=00000100 x5=00000001 x6=fffffff8 x7=fffffffc x8=00000010 x9=00000004 x10=fffffffe x11=00000000 mem0=00000000`
- Log: `results/latest/shift_ops.log`
- HEX: `results/latest/shift_ops.hex`
- VCD: `results/latest/shift_ops.vcd`
