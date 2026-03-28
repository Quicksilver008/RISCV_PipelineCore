# RISCV_PipelineCore Architecture Specification

## Scope

This document describes the current implemented RTL in `src/` as of the refined 5-stage pipeline baseline. It is a design-specification document for the actual core behavior, not a general RISC-V overview.

## Core Summary

- ISA subset: RV32I subset
- Data width: 32 bits
- Register width: 32 bits
- Register count: 32 general-purpose integer registers
- Reset: active-low
- Pipeline depth: 5 stages
- Memory organization: Harvard-style split instruction/data memories
- Branch/jump policy: static not-taken for branches, control transfer resolved in execute

## Pipeline Stages

### 1. Instruction Fetch

Implemented in [`src/Fetch_Cycle.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Fetch_Cycle.v).

Responsibilities:

- Hold and update the program counter
- Read instruction memory using `PC[31:2]`
- Generate `PC + 4`
- Stall the PC and IF/ID register when a load-use hazard is detected
- Flush the IF/ID register on a taken branch

### 2. Instruction Decode / Register Fetch

Implemented in [`src/Decode_cycle.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Decode_cycle.v).

Responsibilities:

- Decode opcode, `funct3`, and `funct7`
- Read the register file
- Generate sign-extended immediates
- Capture control/data signals into the ID/EX register
- Insert a bubble into ID/EX when `FlushE` is asserted

### 3. Execute

Implemented in [`src/Execute_Cycle.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Execute_Cycle.v).

Responsibilities:

- Select forwarded ALU operands
- Perform arithmetic, logical, and compare operations
- Form branch target address
- Resolve `beq`
- Capture execution outputs into the EX/MEM register

### 4. Memory

Implemented in [`src/Memory_Cycle.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Memory_Cycle.v).

Responsibilities:

- Perform word-aligned data memory reads and writes
- Capture memory-stage results into the MEM/WB register

### 5. Writeback

Implemented in [`src/Writeback_Cycle.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Writeback_Cycle.v).

Responsibilities:

- Select final writeback result
- Drive the value written into the register file

## Top-Level Datapath

Top-level integration is in [`src/Pipeline_Top.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Pipeline_Top.v).

Major blocks:

- `fetch_cycle`
- `decode_cycle`
- `execute_cycle`
- `memory_cycle`
- `writeback_cycle`
- `hazard_unit`

The top-level also derives decode-stage source register IDs directly from the fetched instruction for hazard detection.

## Register File Behavior

Implemented in [`src/Register_File.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Register_File.v).

Behavior:

- 32 registers, 32 bits each
- `x0` is hard-wired to zero
- Writes occur on the rising clock edge
- On a same-cycle read/write address match, the read port returns `WD3`

That last point avoids stale reads when decode reads a register in the same cycle that writeback commits it.

## Instruction and Data Memory

### Instruction Memory

Implemented in [`src/Instruction_Memory.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Instruction_Memory.v).

- Depth: 1024 words
- Addressing: `A[31:2]`
- Initialization file: `src/memfile.hex`
- Reset fetch value: `0x00000013` (`addi x0, x0, 0`, treated as NOP)

### Data Memory

Implemented in [`src/dataMemory.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/dataMemory.v).

- Depth: 1024 words
- Addressing: `A[11:2]`
- Access size: word only
- Reset clears the entire memory array

## Supported Instructions

The currently implemented and verified subset is:

| Instruction | Type | Opcode | `funct3` | `funct7` | Notes |
| --- | --- | --- | --- | --- | --- |
| `add`  | R | `0110011` | `000` | `0000000` | ALU add |
| `sub`  | R | `0110011` | `000` | `0100000` | ALU subtract |
| `and`  | R | `0110011` | `111` | `0000000` | Bitwise AND |
| `or`   | R | `0110011` | `110` | `0000000` | Bitwise OR |
| `slt`  | R | `0110011` | `010` | `0000000` | Signed set-less-than |
| `sll`  | R | `0110011` | `001` | `0000000` | Logical left shift |
| `srl`  | R | `0110011` | `101` | `0000000` | Logical right shift |
| `sra`  | R | `0110011` | `101` | `0100000` | Arithmetic right shift |
| `addi` | I | `0010011` | `000` | `-` | Immediate add |
| `slli` | I | `0010011` | `001` | `0000000` | Immediate left shift |
| `srli` | I | `0010011` | `101` | `0000000` | Immediate logical right shift |
| `srai` | I | `0010011` | `101` | `0100000` | Immediate arithmetic right shift |
| `lw`   | I | `0000011` | `010` | `-` | Word load |
| `jalr` | I | `1100111` | `000` | `-` | Register-indirect jump |
| `sw`   | S | `0100011` | `010` | `-` | Word store |
| `beq`  | B | `1100011` | `000` | `-` | Branch equal |
| `jal`  | J | `1101111` | `-` | `-` | PC-relative jump |

## Immediate Formats

Implemented in [`src/Sign_Extend.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Sign_Extend.v).

- `ImmSrc = 2'b00`: I-type immediate
- `ImmSrc = 2'b01`: S-type immediate
- `ImmSrc = 2'b10`: B-type immediate
- `ImmSrc = 2'b11`: J-type immediate

## ALU Control Encoding

The ALU and decoder are implemented in [`src/ALU.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/ALU.v) and [`src/ALudec.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/ALudec.v).

| `ALUControl` | Operation |
| --- | --- |
| `3'b000` | Add |
| `3'b001` | Subtract |
| `3'b010` | AND |
| `3'b011` | OR |
| `3'b100` | SLL |
| `3'b101` | SRL |
| `3'b110` | SRA |
| `3'b111` | SLT |

## Hazard Handling

Implemented in [`src/Hazard_unit.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/Hazard_unit.v).

### Data Hazards

Supported mechanisms:

- EX/MEM to EX forwarding for ALU-producing instructions
- MEM/WB to EX forwarding
- Same-cycle WB to ID register-file bypass
- Load-use detection with one-cycle stall

Load-use behavior:

- If the instruction in execute is a `lw`
- and its destination register matches `rs1` or `rs2` of the instruction in decode
- then the hazard unit asserts `StallF`, `StallD`, and `FlushE`

This freezes fetch/decode and inserts a bubble into execute for one cycle.

### Control Hazards

- `beq` is resolved in the execute stage
- Fetch assumes not-taken
- `jal` and `jalr` are also resolved in the execute stage
- When a branch or jump redirects control flow, the hazard unit asserts `FlushD` and `FlushE`

This removes wrong-path instructions already sitting in IF/ID and ID/EX.

### Structural Hazards

There is no IF-vs-MEM structural hazard in the current implementation because the core uses separate instruction and data memories.

If the project later moves to a single shared memory, explicit arbitration or fetch stalling will need to be added.

## Reset Behavior

The design uses active-low reset consistently:

- PC resets to `0`
- pipeline registers reset to zero or NOP-safe values
- register file resets to all zeroes
- data memory resets to all zeroes

## Verification Baseline

The directed self-checking regression lives in [`src/pipeline_tb.v`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/src/pipeline_tb.v).

The current test program covers:

- `addi`
- ALU result forwarding
- WB-to-ID register-file bypass
- store/load path
- load-use stall
- taken-branch flush

## Known Functional Limits

Not yet implemented:

- byte/halfword loads and stores
- unsigned compares
- multiply/divide
- exceptions or interrupts
- CSRs
- caches
- branch prediction beyond static not-taken

## Recommended Bring-Up Flow

1. Write a program in the supported subset.
2. Assemble it with `riscv_assembler.py`.
3. Write the generated hex into `src/memfile.hex`.
4. Compile with `iverilog`.
5. Run with `vvp`.
6. Inspect waveforms in `dump.vcd` if needed.

## License

Project documentation and source are released under the MIT License. See [`LICENSE`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/LICENSE).
