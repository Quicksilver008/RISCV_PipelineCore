module ALUdecoder(ALUOp,funct3,op,funct7,ALUControl);
    input [6:0] op,funct7;
    input [2:0]funct3;
    input [1:0]ALUOp;
    output [2:0]ALUControl;
    wire concatination;

    assign concatination={op[5],funct7[5]};
    
    assign ALUControl=(ALUOp==2'b00)?3'b000:
                      (ALUOp==2'b01)?3'b001:
                      (ALUOp==2'b10&funct3==3'b010)?3'b101:
                      (ALUOp==2'b10&funct3==3'b110)?3'b011:
                      (ALUOp==2'b10&funct3==3'b111)?3'b010:
                      (ALUOp==2'b10&funct3==3'b000&concatination==2'b11)?3'b001:
                      (ALUOp==2'b10&funct3==3'b000&concatination!=2'b11)?3'b000:000;
                      
endmodule;
