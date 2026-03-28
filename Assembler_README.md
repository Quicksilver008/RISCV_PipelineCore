# RISC-V Assembler Helper

`riscv_assembler.py` is a small utility that converts a restricted RISC-V assembly program into the `memfile.hex` format used by the instruction memory in this project.

## Supported Instructions

- R-type: `add`, `sub`, `and`, `or`, `slt`, `sll`, `srl`, `sra`
- I-type: `addi`, `slli`, `srli`, `srai`, `lw`, `jalr`
- S-type: `sw`
- B-type: `beq`
- J-type: `jal`

## Supported Operand Forms

- `add rd, rs1, rs2`
- `sub rd, rs1, rs2`
- `and rd, rs1, rs2`
- `or rd, rs1, rs2`
- `slt rd, rs1, rs2`
- `sll rd, rs1, rs2`
- `srl rd, rs1, rs2`
- `sra rd, rs1, rs2`
- `addi rd, rs1, imm`
- `slli rd, rs1, shamt`
- `srli rd, rs1, shamt`
- `srai rd, rs1, shamt`
- `lw rd, imm(rs1)`
- `sw rs2, imm(rs1)`
- `beq rs1, rs2, label`
- `jal rd, label`
- `jalr rd, imm(rs1)`

## Usage

Run from the project root:

```bash
python riscv_assembler.py sample_program.asm src/memfile.hex
```

For the full automated firmware test flow:

```bash
python run_firmware_test.py sample_program.asm tests/firmware/sample_program.expect.json
```

For the complete suite:

```bash
python run_firmware_suite.py
```

This writes:

- `@00000000` on the first line
- one 32-bit instruction word per line in uppercase hexadecimal

## Notes

- Labels are supported for `beq`.
- Immediates may be decimal, hexadecimal (`0x...`), or binary (`0b...`).
- This tool is intentionally small and only covers the subset implemented in the core.
- The generated output assumes word-aligned instruction fetch from `src/Instruction_Memory.v`.

## Example

See [`sample_program.asm`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/sample_program.asm) for a small program that exercises ALU operations, store/load, and a taken branch.

Its matching expected architectural state is stored in [`tests/firmware/sample_program.expect.json`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/tests/firmware/sample_program.expect.json).

## License

This helper is distributed with the project under the MIT License. See [`LICENSE`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/LICENSE).
