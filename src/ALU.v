`ifndef ALU_V
`define ALU_V

module ALU(A, B, Result, ALUControl, OverFlow, Carry, Zero, Negative);

    input [31:0] A, B;
    input [2:0] ALUControl;
    output Carry, OverFlow, Zero, Negative;
    output [31:0] Result;

    wire is_subtract;
    wire [31:0] operand_b;
    wire [32:0] sum_extended;
    wire [31:0] sum_result;
    wire signed [31:0] signed_a;
    wire [31:0] sra_result;

    assign is_subtract = (ALUControl == 3'b001) || (ALUControl == 3'b111);
    assign operand_b = is_subtract ? ~B : B;
    assign sum_extended = {1'b0, A} + {1'b0, operand_b} + is_subtract;
    assign sum_result = sum_extended[31:0];
    assign signed_a = A;
    assign sra_result = signed_a >>> B[4:0];

    assign Result = (ALUControl == 3'b000) ? sum_result :
                    (ALUControl == 3'b001) ? sum_result :
                    (ALUControl == 3'b010) ? (A & B) :
                    (ALUControl == 3'b011) ? (A | B) :
                    (ALUControl == 3'b100) ? (A << B[4:0]) :
                    (ALUControl == 3'b101) ? (A >> B[4:0]) :
                    (ALUControl == 3'b110) ? sra_result :
                    (ALUControl == 3'b111) ? {{31{1'b0}}, sum_result[31]} :
                    32'h00000000;

    assign Carry = sum_extended[32];
    assign OverFlow = (ALUControl == 3'b000) ?
                      ((A[31] == B[31]) && (sum_result[31] != A[31])) :
                      (ALUControl == 3'b001 || ALUControl == 3'b111) ?
                      ((A[31] != B[31]) && (sum_result[31] != A[31])) :
                      1'b0;
    assign Zero = (Result == 32'h00000000);
    assign Negative = Result[31];

endmodule

`endif
