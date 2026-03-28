`ifndef REGISTER_FILE_V
`define REGISTER_FILE_V

module Register_File(clk, rst, WE3, WD3, A1, A2, A3, RD1, RD2);

    input clk, rst, WE3;
    input [4:0] A1, A2, A3;
    input [31:0] WD3;
    output [31:0] RD1, RD2;

    reg [31:0] registers [31:0];
    integer i;

    always @(posedge clk or negedge rst) begin
        if (!rst) begin
            for (i = 0; i < 32; i = i + 1) begin
                registers[i] <= 32'h00000000;
            end
        end else if (WE3 && (A3 != 5'd0)) begin
            registers[A3] <= WD3;
        end
    end

    assign RD1 = (A1 == 5'd0) ? 32'h00000000 :
                 (WE3 && (A3 != 5'd0) && (A3 == A1)) ? WD3 :
                 registers[A1];
    assign RD2 = (A2 == 5'd0) ? 32'h00000000 :
                 (WE3 && (A3 != 5'd0) && (A3 == A2)) ? WD3 :
                 registers[A2];

endmodule

`endif
