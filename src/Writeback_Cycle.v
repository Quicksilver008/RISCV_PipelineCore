`ifndef WRITEBACK_CYCLE_V
`define WRITEBACK_CYCLE_V

module writeback_cycle(ResultSrcW, PCPlus4W, ALU_ResultW, ReadDataW, ResultW);

    input [1:0] ResultSrcW;
    input [31:0] PCPlus4W, ALU_ResultW, ReadDataW;
    output [31:0] ResultW;
    reg [31:0] ResultW;

    always @(*) begin
        case (ResultSrcW)
            2'b00: ResultW = ALU_ResultW;
            2'b01: ResultW = ReadDataW;
            2'b10: ResultW = PCPlus4W;
            default: ResultW = 32'h00000000;
        endcase
    end

endmodule

`endif
