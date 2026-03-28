`ifndef FETCH_CYCLE_V
`define FETCH_CYCLE_V

`include "mux2to1.v"
`include "PC.v"
`include "Instruction_Memory.v"
`include "PC_Adder.v"

module fetch_cycle(clk, rst, StallF, StallD, FlushD, PCSrcE, PCTargetE, InstrD, PCD, PCPlus4D);

    input clk, rst, StallF, StallD, FlushD, PCSrcE;
    input [31:0] PCTargetE;
    output [31:0] InstrD;
    output [31:0] PCD, PCPlus4D;

    wire [31:0] PCNextF, PCF, PCPlus4F, InstrF;
    reg [31:0] InstrF_reg;
    reg [31:0] PCF_reg, PCPlus4F_reg;

    Mux PC_MUX(
        .a(PCPlus4F),
        .b(PCTargetE),
        .s(PCSrcE),
        .c(PCNextF)
    );

    PC_Module Program_Counter(
        .clk(clk),
        .rst(rst),
        .en(!StallF),
        .PC(PCF),
        .PC_Next(PCNextF)
    );

    Instruction_Memory IMEM(
        .rst(rst),
        .A(PCF),
        .RD(InstrF)
    );

    PC_Adder PC_adder(
        .a(PCF),
        .b(32'h00000004),
        .c(PCPlus4F)
    );

    always @(posedge clk or negedge rst) begin
        if (!rst) begin
            InstrF_reg <= 32'h00000013;
            PCF_reg <= 32'h00000000;
            PCPlus4F_reg <= 32'h00000000;
        end else if (FlushD) begin
            InstrF_reg <= 32'h00000013;
            PCF_reg <= 32'h00000000;
            PCPlus4F_reg <= 32'h00000000;
        end else if (!StallD) begin
            InstrF_reg <= InstrF;
            PCF_reg <= PCF;
            PCPlus4F_reg <= PCPlus4F;
        end
    end

    assign InstrD = InstrF_reg;
    assign PCD = PCF_reg;
    assign PCPlus4D = PCPlus4F_reg;

endmodule

`endif
