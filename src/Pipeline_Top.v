`ifndef PIPELINE_TOP_V
`define PIPELINE_TOP_V

`include "Fetch_Cycle.v"
`include "Decode_cycle.v"
`include "Execute_Cycle.v"
`include "Memory_Cycle.v"
`include "Writeback_Cycle.v"
`include "Hazard_unit.v"

module Pipeline_top(clk, rst);

    input clk, rst;

    wire PCSrcE;
    wire StallF, StallD, FlushD, FlushE;
    wire RegWriteW, RegWriteE, ALUSrcE, MemWriteE, BranchE, JumpE, JumpRegE, RegWriteM, MemWriteM;
    wire UseRs1D, UseRs2D;
    wire [1:0] ResultSrcE, ResultSrcM, ResultSrcW;
    wire [2:0] ALUControlE;
    wire [4:0] RD_E, RD_M, RDW;
    wire [4:0] RS1_D, RS2_D, RS1_E, RS2_E;
    wire [1:0] ForwardBE, ForwardAE;
    wire [31:0] PCTargetE, InstrD, PCD, PCPlus4D;
    wire [31:0] ResultW, RD1_E, RD2_E, Imm_Ext_E, PCE, PCPlus4E;
    wire [31:0] PCPlus4M, WriteDataM, ALU_ResultM;
    wire [31:0] PCPlus4W, ALU_ResultW, ReadDataW;
    wire [31:0] ForwardValueM;
    wire [6:0] OpD;

    assign RS1_D = InstrD[19:15];
    assign RS2_D = InstrD[24:20];
    assign OpD = InstrD[6:0];
    assign UseRs1D = (OpD == 7'b0110011) ||
                     (OpD == 7'b0010011) ||
                     (OpD == 7'b0000011) ||
                     (OpD == 7'b0100011) ||
                     (OpD == 7'b1100011) ||
                     (OpD == 7'b1100111);
    assign UseRs2D = (OpD == 7'b0110011) ||
                     (OpD == 7'b0100011) ||
                     (OpD == 7'b1100011);
    assign ForwardValueM = (ResultSrcM == 2'b10) ? PCPlus4M : ALU_ResultM;

    fetch_cycle Fetch(
        .clk(clk),
        .rst(rst),
        .StallF(StallF),
        .StallD(StallD),
        .FlushD(FlushD),
        .PCSrcE(PCSrcE),
        .PCTargetE(PCTargetE),
        .InstrD(InstrD),
        .PCD(PCD),
        .PCPlus4D(PCPlus4D)
    );

    decode_cycle Decode(
        .clk(clk),
        .rst(rst),
        .FlushE(FlushE),
        .InstrD(InstrD),
        .PCD(PCD),
        .PCPlus4D(PCPlus4D),
        .RegWriteW(RegWriteW),
        .RDW(RDW),
        .ResultW(ResultW),
        .RegWriteE(RegWriteE),
        .ALUSrcE(ALUSrcE),
        .MemWriteE(MemWriteE),
        .ResultSrcE(ResultSrcE),
        .BranchE(BranchE),
        .JumpE(JumpE),
        .JumpRegE(JumpRegE),
        .ALUControlE(ALUControlE),
        .RD1_E(RD1_E),
        .RD2_E(RD2_E),
        .Imm_Ext_E(Imm_Ext_E),
        .RD_E(RD_E),
        .PCE(PCE),
        .PCPlus4E(PCPlus4E),
        .RS1_E(RS1_E),
        .RS2_E(RS2_E)
    );

    execute_cycle Execute(
        .clk(clk),
        .rst(rst),
        .RegWriteE(RegWriteE),
        .ALUSrcE(ALUSrcE),
        .MemWriteE(MemWriteE),
        .ResultSrcE(ResultSrcE),
        .BranchE(BranchE),
        .JumpE(JumpE),
        .JumpRegE(JumpRegE),
        .ALUControlE(ALUControlE),
        .RD1_E(RD1_E),
        .RD2_E(RD2_E),
        .Imm_Ext_E(Imm_Ext_E),
        .RD_E(RD_E),
        .PCE(PCE),
        .PCPlus4E(PCPlus4E),
        .PCSrcE(PCSrcE),
        .PCTargetE(PCTargetE),
        .RegWriteM(RegWriteM),
        .MemWriteM(MemWriteM),
        .ResultSrcM(ResultSrcM),
        .RD_M(RD_M),
        .PCPlus4M(PCPlus4M),
        .WriteDataM(WriteDataM),
        .ALU_ResultM(ALU_ResultM),
        .ResultW(ResultW),
        .ForwardValueM(ForwardValueM),
        .ForwardA_E(ForwardAE),
        .ForwardB_E(ForwardBE)
    );

    memory_cycle Memory(
        .clk(clk),
        .rst(rst),
        .RegWriteM(RegWriteM),
        .MemWriteM(MemWriteM),
        .ResultSrcM(ResultSrcM),
        .RD_M(RD_M),
        .PCPlus4M(PCPlus4M),
        .WriteDataM(WriteDataM),
        .ALU_ResultM(ALU_ResultM),
        .RegWriteW(RegWriteW),
        .ResultSrcW(ResultSrcW),
        .RD_W(RDW),
        .PCPlus4W(PCPlus4W),
        .ALU_ResultW(ALU_ResultW),
        .ReadDataW(ReadDataW)
    );

    writeback_cycle WriteBack(
        .ResultSrcW(ResultSrcW),
        .PCPlus4W(PCPlus4W),
        .ALU_ResultW(ALU_ResultW),
        .ReadDataW(ReadDataW),
        .ResultW(ResultW)
    );

    hazard_unit Hazard(
        .rst(rst),
        .PCSrcE(PCSrcE),
        .RegWriteM(RegWriteM),
        .RegWriteW(RegWriteW),
        .ResultSrcE(ResultSrcE),
        .ResultSrcM(ResultSrcM),
        .UseRs1D(UseRs1D),
        .UseRs2D(UseRs2D),
        .RD_E(RD_E),
        .RD_M(RD_M),
        .RD_W(RDW),
        .Rs1_D(RS1_D),
        .Rs2_D(RS2_D),
        .Rs1_E(RS1_E),
        .Rs2_E(RS2_E),
        .StallF(StallF),
        .StallD(StallD),
        .FlushD(FlushD),
        .FlushE(FlushE),
        .ForwardAE(ForwardAE),
        .ForwardBE(ForwardBE)
    );

endmodule

`endif
