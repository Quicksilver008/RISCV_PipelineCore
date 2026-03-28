#!/usr/bin/env python3
"""
RISC-V Assembly to Machine Code Converter
For RISCV_PipelineCore Processor

Supported Instructions:
- R-type: add, sub, and, or, slt
- R-type shifts: sll, srl, sra
- I-type: addi, lw (load word)
- I-type shifts: slli, srli, srai
- S-type: sw (store word)
- B-type: beq (branch if equal)
- J-type: jal, jalr

Usage: python riscv_assembler.py input.asm output.hex
"""

import sys
import re
from typing import Dict, List, Tuple

class RISC_V_Assembler:
    def __init__(self):
        # Register mapping
        self.registers = {
            'zero': 0, 'x0': 0,
            'ra': 1, 'x1': 1,
            'sp': 2, 'x2': 2,
            'gp': 3, 'x3': 3,
            'tp': 4, 'x4': 4,
            't0': 5, 'x5': 5,
            't1': 6, 'x6': 6,
            't2': 7, 'x7': 7,
            's0': 8, 'fp': 8, 'x8': 8,
            's1': 9, 'x9': 9,
            'a0': 10, 'x10': 10,
            'a1': 11, 'x11': 11,
            'a2': 12, 'x12': 12,
            'a3': 13, 'x13': 13,
            'a4': 14, 'x14': 14,
            'a5': 15, 'x15': 15,
            'a6': 16, 'x16': 16,
            'a7': 17, 'x17': 17,
            's2': 18, 'x18': 18,
            's3': 19, 'x19': 19,
            's4': 20, 'x20': 20,
            's5': 21, 'x21': 21,
            's6': 22, 'x22': 22,
            's7': 23, 'x23': 23,
            's8': 24, 'x24': 24,
            's9': 25, 'x25': 25,
            's10': 26, 'x26': 26,
            's11': 27, 'x27': 27,
            't3': 28, 'x28': 28,
            't4': 29, 'x29': 29,
            't5': 30, 'x30': 30,
            't6': 31, 'x31': 31
        }

        # Instruction opcodes and funct fields
        self.opcodes = {
            'add': {'opcode': 0b0110011, 'funct3': 0b000, 'funct7': 0b0000000},
            'sub': {'opcode': 0b0110011, 'funct3': 0b000, 'funct7': 0b0100000},
            'and': {'opcode': 0b0110011, 'funct3': 0b111, 'funct7': 0b0000000},
            'or':  {'opcode': 0b0110011, 'funct3': 0b110, 'funct7': 0b0000000},
            'slt': {'opcode': 0b0110011, 'funct3': 0b010, 'funct7': 0b0000000},
            'sll': {'opcode': 0b0110011, 'funct3': 0b001, 'funct7': 0b0000000},
            'srl': {'opcode': 0b0110011, 'funct3': 0b101, 'funct7': 0b0000000},
            'sra': {'opcode': 0b0110011, 'funct3': 0b101, 'funct7': 0b0100000},
            'addi': {'opcode': 0b0010011, 'funct3': 0b000},
            'slli': {'opcode': 0b0010011, 'funct3': 0b001, 'funct7': 0b0000000},
            'srli': {'opcode': 0b0010011, 'funct3': 0b101, 'funct7': 0b0000000},
            'srai': {'opcode': 0b0010011, 'funct3': 0b101, 'funct7': 0b0100000},
            'lw':  {'opcode': 0b0000011, 'funct3': 0b010},
            'sw':  {'opcode': 0b0100011, 'funct3': 0b010},
            'beq': {'opcode': 0b1100011, 'funct3': 0b000},
            'jal': {'opcode': 0b1101111},
            'jalr': {'opcode': 0b1100111, 'funct3': 0b000}
        }

        # Labels and their addresses
        self.labels = {}
        self.current_address = 0

    def parse_register(self, reg: str) -> int:
        """Parse register name to number"""
        if reg not in self.registers:
            raise ValueError(f"Unknown register: {reg}")
        return self.registers[reg]

    def parse_immediate(self, imm: str) -> int:
        """Parse immediate value (decimal or hex)"""
        if imm.startswith('0x'):
            return int(imm, 16)
        elif imm.startswith('0b'):
            return int(imm, 2)
        else:
            return int(imm)

    def assemble_r_type(self, instr: str, rd: str, rs1: str, rs2: str) -> int:
        """Assemble R-type instruction: instr rd, rs1, rs2"""
        opcode = self.opcodes[instr]['opcode']
        funct3 = self.opcodes[instr]['funct3']
        funct7 = self.opcodes[instr]['funct7']

        rd_num = self.parse_register(rd)
        rs1_num = self.parse_register(rs1)
        rs2_num = self.parse_register(rs2)

        # R-type format: funct7[31:25] rs2[24:20] rs1[19:15] funct3[14:12] rd[11:7] opcode[6:0]
        machine_code = (funct7 << 25) | (rs2_num << 20) | (rs1_num << 15) | (funct3 << 12) | (rd_num << 7) | opcode
        return machine_code

    def assemble_i_type(self, instr: str, rd: str, imm: str, rs1: str) -> int:
        """Assemble I-type instruction"""
        opcode = self.opcodes[instr]['opcode']
        funct3 = self.opcodes[instr]['funct3']

        rd_num = self.parse_register(rd)
        rs1_num = self.parse_register(rs1)
        imm_val = self.parse_immediate(imm)

        # I-type format: imm[31:20] rs1[19:15] funct3[14:12] rd[11:7] opcode[6:0]
        # For 12-bit immediate
        imm_12bit = imm_val & 0xFFF
        machine_code = (imm_12bit << 20) | (rs1_num << 15) | (funct3 << 12) | (rd_num << 7) | opcode
        return machine_code

    def assemble_shift_i_type(self, instr: str, rd: str, rs1: str, shamt: str) -> int:
        """Assemble I-type shift instruction: instr rd, rs1, shamt"""
        opcode = self.opcodes[instr]['opcode']
        funct3 = self.opcodes[instr]['funct3']
        funct7 = self.opcodes[instr]['funct7']

        rd_num = self.parse_register(rd)
        rs1_num = self.parse_register(rs1)
        shamt_val = self.parse_immediate(shamt)

        if shamt_val < 0 or shamt_val > 31:
            raise ValueError("Shift amount must be in the range 0..31")

        machine_code = (funct7 << 25) | (shamt_val << 20) | (rs1_num << 15) | (funct3 << 12) | (rd_num << 7) | opcode
        return machine_code

    def assemble_s_type(self, instr: str, rs2: str, imm: str, rs1: str) -> int:
        """Assemble S-type instruction: instr rs2, imm(rs1)"""
        opcode = self.opcodes[instr]['opcode']
        funct3 = self.opcodes[instr]['funct3']

        rs1_num = self.parse_register(rs1)
        rs2_num = self.parse_register(rs2)
        imm_val = self.parse_immediate(imm)

        # S-type format: imm[31:25] rs2[24:20] rs1[19:15] funct3[14:12] imm[11:7] opcode[6:0]
        imm_11_5 = (imm_val >> 5) & 0x7F  # bits 11:5
        imm_4_0 = imm_val & 0x1F          # bits 4:0

        machine_code = (imm_11_5 << 25) | (rs2_num << 20) | (rs1_num << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
        return machine_code

    def assemble_b_type(self, instr: str, rs1: str, rs2: str, label: str) -> int:
        """Assemble B-type instruction: instr rs1, rs2, label"""
        opcode = self.opcodes[instr]['opcode']
        funct3 = self.opcodes[instr]['funct3']

        rs1_num = self.parse_register(rs1)
        rs2_num = self.parse_register(rs2)

        # Calculate branch offset in bytes relative to the current PC.
        if label in self.labels:
            target_addr = self.labels[label]
            offset = target_addr - self.current_address
        else:
            raise ValueError(f"Undefined label: {label}")

        if offset & 0x1:
            raise ValueError("Branch target must be 2-byte aligned")

        # B-type format:
        # imm[12] at bit 31
        # imm[10:5] at bits 30:25
        # rs2 at bits 24:20
        # rs1 at bits 19:15
        # funct3 at bits 14:12
        # imm[4:1] at bits 11:8
        # imm[11] at bit 7
        imm_12 = (offset >> 11) & 0x1
        imm_10_5 = (offset >> 5) & 0x3F
        imm_4_1 = (offset >> 1) & 0xF
        imm_11 = (offset >> 10) & 0x1

        machine_code = (
            (imm_12 << 31) |
            (imm_10_5 << 25) |
            (rs2_num << 20) |
            (rs1_num << 15) |
            (funct3 << 12) |
            (imm_4_1 << 8) |
            (imm_11 << 7) |
            opcode
        )
        return machine_code

    def assemble_j_type(self, instr: str, rd: str, label: str) -> int:
        """Assemble J-type instruction: jal rd, label"""
        opcode = self.opcodes[instr]['opcode']
        rd_num = self.parse_register(rd)

        if label not in self.labels:
            raise ValueError(f"Undefined label: {label}")

        offset = self.labels[label] - self.current_address
        if offset & 0x1:
            raise ValueError("Jump target must be 2-byte aligned")

        imm_20 = (offset >> 20) & 0x1
        imm_10_1 = (offset >> 1) & 0x3FF
        imm_11 = (offset >> 11) & 0x1
        imm_19_12 = (offset >> 12) & 0xFF

        machine_code = (
            (imm_20 << 31) |
            (imm_19_12 << 12) |
            (imm_11 << 20) |
            (imm_10_1 << 21) |
            (rd_num << 7) |
            opcode
        )
        return machine_code

    def parse_instruction(self, line: str) -> int:
        """Parse a single assembly instruction"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None

        # Remove comments
        line = line.split('#')[0].strip()

        # Check for labels
        if ':' in line:
            label, rest = line.split(':', 1)
            label = label.strip()
            self.labels[label] = self.current_address
            if rest.strip():
                line = rest.strip()
            else:
                return None

        parts = line.replace(',', ' ').split()
        if not parts:
            return None

        instr = parts[0].lower()

        try:
            if instr in ['add', 'sub', 'and', 'or', 'slt', 'sll', 'srl', 'sra']:
                # R-type: instr rd, rs1, rs2
                rd, rs1, rs2 = parts[1], parts[2], parts[3]
                return self.assemble_r_type(instr, rd, rs1, rs2)

            elif instr == 'addi':
                # I-type ALU: addi rd, rs1, imm
                rd, rs1, imm = parts[1], parts[2], parts[3]
                return self.assemble_i_type(instr, rd, imm, rs1)

            elif instr in ['slli', 'srli', 'srai']:
                rd, rs1, shamt = parts[1], parts[2], parts[3]
                return self.assemble_shift_i_type(instr, rd, rs1, shamt)

            elif instr == 'lw':
                # I-type: lw rd, imm(rs1)
                rd = parts[1]
                imm_rs1 = parts[2]
                imm, rs1 = imm_rs1.split('(')
                rs1 = rs1.rstrip(')')
                return self.assemble_i_type(instr, rd, imm, rs1)

            elif instr == 'sw':
                # S-type: sw rs2, imm(rs1)
                rs2 = parts[1]
                imm_rs1 = parts[2]
                imm, rs1 = imm_rs1.split('(')
                rs1 = rs1.rstrip(')')
                return self.assemble_s_type(instr, rs2, imm, rs1)

            elif instr == 'beq':
                # B-type: beq rs1, rs2, label
                rs1, rs2, label = parts[1], parts[2], parts[3]
                return self.assemble_b_type(instr, rs1, rs2, label)

            elif instr == 'jal':
                rd, label = parts[1], parts[2]
                return self.assemble_j_type(instr, rd, label)

            elif instr == 'jalr':
                rd = parts[1]
                imm_rs1 = parts[2]
                imm, rs1 = imm_rs1.split('(')
                rs1 = rs1.rstrip(')')
                return self.assemble_i_type(instr, rd, imm, rs1)

            else:
                raise ValueError(f"Unsupported instruction: {instr}")

        except Exception as e:
            raise ValueError(f"Error parsing instruction '{line}': {str(e)}")

    def assemble_file(self, input_file: str, output_file: str):
        """Assemble assembly file to machine code"""
        print(f"Assembling {input_file} -> {output_file}")

        # First pass: collect labels and count instructions
        self.labels = {}
        self.current_address = 0
        instructions = []

        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # Remove comments
                    line = line.split('#')[0].strip()

                    # Check for labels
                    if ':' in line:
                        label, rest = line.split(':', 1)
                        label = label.strip()
                        if label in self.labels:
                            raise ValueError(f"Duplicate label: {label}")
                        self.labels[label] = self.current_address
                        if rest.strip():
                            line = rest.strip()
                        else:
                            continue

                    # Parse instruction to count it
                    parts = line.replace(',', ' ').split()
                    if not parts:
                        continue

                    instr = parts[0].lower()
                    if instr in ['add', 'sub', 'and', 'or', 'slt', 'sll', 'srl', 'sra', 'addi', 'slli', 'srli', 'srai', 'lw', 'sw', 'beq', 'jal', 'jalr']:
                        instructions.append((line, self.current_address))
                        self.current_address += 4

                except Exception as e:
                    raise ValueError(f"Error on line {line_num}: {str(e)}")

        # Second pass: generate machine code
        machine_codes = []
        self.current_address = 0

        for line, addr in instructions:
            self.current_address = addr
            parts = line.replace(',', ' ').split()
            instr = parts[0].lower()

            try:
                if instr in ['add', 'sub', 'and', 'or', 'slt', 'sll', 'srl', 'sra']:
                    # R-type: instr rd, rs1, rs2
                    rd, rs1, rs2 = parts[1], parts[2], parts[3]
                    machine_codes.append(self.assemble_r_type(instr, rd, rs1, rs2))

                elif instr == 'addi':
                    rd, rs1, imm = parts[1], parts[2], parts[3]
                    machine_codes.append(self.assemble_i_type(instr, rd, imm, rs1))

                elif instr in ['slli', 'srli', 'srai']:
                    rd, rs1, shamt = parts[1], parts[2], parts[3]
                    machine_codes.append(self.assemble_shift_i_type(instr, rd, rs1, shamt))

                elif instr == 'lw':
                    # I-type: lw rd, imm(rs1)
                    rd = parts[1]
                    imm_rs1 = parts[2]
                    imm, rs1 = imm_rs1.split('(')
                    rs1 = rs1.rstrip(')')
                    machine_codes.append(self.assemble_i_type(instr, rd, imm, rs1))

                elif instr == 'sw':
                    # S-type: sw rs2, imm(rs1)
                    rs2 = parts[1]
                    imm_rs1 = parts[2]
                    imm, rs1 = imm_rs1.split('(')
                    rs1 = rs1.rstrip(')')
                    machine_codes.append(self.assemble_s_type(instr, rs2, imm, rs1))

                elif instr == 'beq':
                    # B-type: beq rs1, rs2, label
                    rs1, rs2, label = parts[1], parts[2], parts[3]
                    machine_codes.append(self.assemble_b_type(instr, rs1, rs2, label))

                elif instr == 'jal':
                    rd, label = parts[1], parts[2]
                    machine_codes.append(self.assemble_j_type(instr, rd, label))

                elif instr == 'jalr':
                    rd = parts[1]
                    imm_rs1 = parts[2]
                    imm, rs1 = imm_rs1.split('(')
                    rs1 = rs1.rstrip(')')
                    machine_codes.append(self.assemble_i_type(instr, rd, imm, rs1))

            except Exception as e:
                raise ValueError(f"Error assembling instruction '{line}': {str(e)}")

        # Write output in hex format
        with open(output_file, 'w') as f:
            f.write(f"@00000000\n")
            for code in machine_codes:
                f.write(f"{code:08X}\n")

        print(f"Assembly complete. Generated {len(machine_codes)} instructions.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python riscv_assembler.py input.asm output.hex")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    assembler = RISC_V_Assembler()

    try:
        assembler.assemble_file(input_file, output_file)
        print("Assembly successful!")
    except Exception as e:
        print(f"Assembly failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
