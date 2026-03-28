`ifndef PC_ADDER_V
`define PC_ADDER_V

module PC_Adder(a, b, c);

    input [31:0] a, b;
    output [31:0] c;

    assign c = a + b;

endmodule

`endif
