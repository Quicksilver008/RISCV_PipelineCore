`ifndef PC_V
`define PC_V

module PC_Module(clk, rst, en, PC, PC_Next);

    input clk, rst, en;
    input [31:0] PC_Next;
    output [31:0] PC;
    reg [31:0] PC;

    always @(posedge clk or negedge rst) begin
        if (!rst) begin
            PC <= 32'h00000000;
        end else if (en) begin
            PC <= PC_Next;
        end
    end

endmodule

`endif
