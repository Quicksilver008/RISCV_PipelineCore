`ifndef MAINDEC_V
`define MAINDEC_V

module mainDec(op, RegWrite, MemWrite, ResultSrc, ALUSrc, ImmSrc, ALUOp, Branch, Jump, JumpReg);

    input [6:0] op;
    output RegWrite, MemWrite, ALUSrc, Branch, Jump, JumpReg;
    output [1:0] ResultSrc, ImmSrc, ALUOp;
    reg RegWrite, MemWrite, ALUSrc, Branch, Jump, JumpReg;
    reg [1:0] ResultSrc, ImmSrc, ALUOp;

    always @(*) begin
        RegWrite = 1'b0;
        MemWrite = 1'b0;
        ResultSrc = 2'b00;
        ALUSrc = 1'b0;
        ImmSrc = 2'b00;
        ALUOp = 2'b00;
        Branch = 1'b0;
        Jump = 1'b0;
        JumpReg = 1'b0;

        case (op)
            7'b0000011: begin
                RegWrite = 1'b1;
                ResultSrc = 2'b01;
                ALUSrc = 1'b1;
                ImmSrc = 2'b00;
                ALUOp = 2'b00;
            end
            7'b0100011: begin
                MemWrite = 1'b1;
                ALUSrc = 1'b1;
                ImmSrc = 2'b01;
                ALUOp = 2'b00;
            end
            7'b0110011: begin
                RegWrite = 1'b1;
                ALUOp = 2'b10;
            end
            7'b0010011: begin
                RegWrite = 1'b1;
                ALUSrc = 1'b1;
                ImmSrc = 2'b00;
                ALUOp = 2'b10;
            end
            7'b1100011: begin
                Branch = 1'b1;
                ImmSrc = 2'b10;
                ALUOp = 2'b01;
            end
            7'b1101111: begin
                RegWrite = 1'b1;
                ResultSrc = 2'b10;
                ImmSrc = 2'b11;
                Jump = 1'b1;
            end
            7'b1100111: begin
                RegWrite = 1'b1;
                ResultSrc = 2'b10;
                ALUSrc = 1'b1;
                ImmSrc = 2'b00;
                Jump = 1'b1;
                JumpReg = 1'b1;
            end
            default: begin
            end
        endcase
    end

endmodule

`endif
