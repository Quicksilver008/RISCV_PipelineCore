`ifndef INSTRUCTION_MEMORY_V
`define INSTRUCTION_MEMORY_V

module Instruction_Memory(rst, A, RD);

    input rst;
    input [31:0] A;
    output [31:0] RD;

    reg [31:0] mem [0:1023];
    integer i;

    assign RD = rst ? mem[A[31:2]] : 32'h00000013;

    initial begin
        for (i = 0; i < 1024; i = i + 1) begin
            mem[i] = 32'h00000013;
        end
        $readmemh("memfile.hex", mem);
    end

endmodule

`endif
