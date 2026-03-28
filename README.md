
# RISCV_PipelineCore

`RISCV_PipelineCore` is a refined 32-bit 5-stage pipelined RISC-V processor implementing a focused RV32I subset. The project is organized as synthesizable Verilog RTL in `src/`, with a small assembler helper and a self-checking simulation flow for bring-up and regression.

## Collaborators

- Mohammad Omar Sulemani
- Md Atib Kaif
- Abhishek Garg

## Implemented Core Features

- 5-stage pipeline: IF, ID, EX, MEM, WB
- 32-bit datapath and 32 integer registers
- Active-low reset
- Separate instruction and data memories
- Static not-taken branch policy
- EX/MEM and MEM/WB forwarding
- Load-use stall insertion
- Branch flush handling
- Self-checking simulation testbench

## Supported Instruction Subset

- R-type: `add`, `sub`, `and`, `or`, `slt`, `sll`, `srl`, `sra`
- I-type: `addi`, `slli`, `srli`, `srai`, `lw`, `jalr`
- S-type: `sw`
- B-type: `beq`
- J-type: `jal`

## Project Layout

- [`src/`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src): RTL, testbench, and instruction hex
- [`docs/CORE_ARCHITECTURE.md`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/docs/CORE_ARCHITECTURE.md): architecture and functionality specification
- [`riscv_assembler.py`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/riscv_assembler.py): subset assembler for generating `memfile.hex`
- [`Assembler_README.md`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/Assembler_README.md): assembler usage notes
- [`sample_program.asm`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/sample_program.asm): example firmware program

## Documentation

The primary design specification is:

- [`docs/CORE_ARCHITECTURE.md`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/docs/CORE_ARCHITECTURE.md)

It covers:

- core architecture
- pipeline stage behavior
- hazard handling
- supported instructions and opcode fields
- ALU control encoding
- memory organization
- reset behavior
- current limitations

## Simulation Flow

From the project `src` directory:

```bash
iverilog -o out_check.vvp pipeline_tb.v
vvp out_check.vvp
```

The testbench writes a waveform dump to `dump.vcd` and checks the final architectural state automatically.

## Firmware-to-Hex Flow

From the project root:

```bash
python riscv_assembler.py sample_program.asm src/memfile.hex
```

Then run simulation again:

```bash
cd src
iverilog -o out_check.vvp pipeline_tb.v
vvp out_check.vvp
```

## Recommended Automated Test Flow

Use assembly-based firmware tests first, not C.

Why:

- the current core only implements a compact RV32I subset
- a C compiler will usually emit unsupported instructions such as `lui`, `auipc`, `jal`, `jalr`, more branch variants, and ABI-related stack/setup code
- there is not yet a linker script, startup runtime, or a full enough ISA subset to make C bring-up efficient

The recommended flow today is:

```bash
python run_firmware_test.py sample_program.asm tests/firmware/sample_program.expect.json
```

This command:

- assembles the firmware into `src/memfile.hex`
- generates simulation expectation files for the testbench
- compiles the RTL with `iverilog`
- runs the simulation with `vvp`
- reports pass/fail

Once the core supports a larger RV32I subset plus startup/linker support, moving to compiled C tests will make sense.

For the full current regression suite:

```bash
python run_firmware_suite.py
```

That command runs every firmware test in `tests/firmware/` and writes logs plus a suite summary into `results/latest/`.

## Current Verification Baseline

The default regression program exercises:

- immediate arithmetic
- ALU RAW forwarding
- register and immediate shift operations
- writeback-to-decode register bypass
- store/load correctness
- load-use stall behavior
- taken branch flush behavior
- `jal` and `jalr` control-flow behavior

## Notes

- The current design is a Harvard-style core, so classical instruction-fetch vs data-memory structural hazards are avoided by construction.
- Only word-aligned memory accesses are implemented.
- Jumps, shifts, CSRs, interrupts, and the rest of RV32I are not yet implemented.

## License

This project is released under the MIT License. See [`LICENSE`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/LICENSE).
