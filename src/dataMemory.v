`ifndef DATA_MEMORY_V
`define DATA_MEMORY_V

module Data_Memory(clk, rst, WE, WD, A, RD);

    input clk, rst, WE;
    input [31:0] A, WD;
    output [31:0] RD;

    reg [31:0] mem [0:1023];
    integer i;
    wire [9:0] word_addr;

    assign word_addr = A[11:2];

    always @(posedge clk or negedge rst) begin
        if (!rst) begin
            for (i = 0; i < 1024; i = i + 1) begin
                mem[i] <= 32'h00000000;
            end
        end else if (WE) begin
            mem[word_addr] <= WD;
        end
    end

    assign RD = rst ? mem[word_addr] : 32'h00000000;

endmodule

`endif
