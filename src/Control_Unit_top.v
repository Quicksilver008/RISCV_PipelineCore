`ifndef CONTROL_UNIT_TOP_V
`define CONTROL_UNIT_TOP_V

`include "ALudec.v"
`include "mainDec.v"

module Control_Unit_Top(Op, funct3, funct7, RegWrite, ImmSrc, ALUSrc, MemWrite, ResultSrc, Branch, Jump, JumpReg, ALUControl);

    input [6:0] Op, funct7;
    input [2:0] funct3;
    output RegWrite, ALUSrc, MemWrite, Branch, Jump, JumpReg;
    output [1:0] ImmSrc, ResultSrc;
    output [2:0] ALUControl;

    wire [1:0] ALUOp;

    mainDec Main_Decoder(
        .op(Op),
        .RegWrite(RegWrite),
        .MemWrite(MemWrite),
        .ResultSrc(ResultSrc),
        .ALUSrc(ALUSrc),
        .ImmSrc(ImmSrc),
        .ALUOp(ALUOp),
        .Branch(Branch),
        .Jump(Jump),
        .JumpReg(JumpReg)
    );

    ALUdecoder ALU_Decoder(
        .ALUOp(ALUOp),
        .funct3(funct3),
        .funct7(funct7),
        .op(Op),
        .ALUControl(ALUControl)
    );

endmodule

`endif
