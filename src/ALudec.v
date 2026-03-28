`ifndef ALUDEC_V
`define ALUDEC_V

module ALUdecoder(ALUOp, funct3, op, funct7, ALUControl);

    input [6:0] op, funct7;
    input [2:0] funct3;
    input [1:0] ALUOp;
    output [2:0] ALUControl;
    reg [2:0] ALUControl;

    always @(*) begin
        case (ALUOp)
            2'b00: ALUControl = 3'b000;
            2'b01: ALUControl = 3'b001;
            2'b10: begin
                case (funct3)
                    3'b000: ALUControl = (op[5] && funct7[5]) ? 3'b001 : 3'b000;
                    3'b001: ALUControl = 3'b100;
                    3'b010: ALUControl = 3'b111;
                    3'b101: ALUControl = funct7[5] ? 3'b110 : 3'b101;
                    3'b110: ALUControl = 3'b011;
                    3'b111: ALUControl = 3'b010;
                    default: ALUControl = 3'b000;
                endcase
            end
            default: ALUControl = 3'b000;
        endcase
    end

endmodule

`endif
