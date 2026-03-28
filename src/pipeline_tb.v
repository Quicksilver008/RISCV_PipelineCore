`include "Pipeline_Top.v"
`include "test_config.vh"

module tb();

    reg clk;
    reg rst;

    Pipeline_top dut(.clk(clk), .rst(rst));

    always #5 clk = ~clk;

    initial begin
        clk = 1'b0;
        rst = 1'b0;
        #20;
        rst = 1'b1;
    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, tb);
    end

    initial begin
        @(posedge rst);
        repeat (`TEST_CYCLES) @(posedge clk);

        $display("x0=%h x1=%h x2=%h x3=%h x4=%h x5=%h x6=%h x7=%h x8=%h x9=%h x10=%h x11=%h mem0=%h",
                 dut.Decode.rf.registers[0],
                 dut.Decode.rf.registers[1],
                 dut.Decode.rf.registers[2],
                 dut.Decode.rf.registers[3],
                 dut.Decode.rf.registers[4],
                 dut.Decode.rf.registers[5],
                 dut.Decode.rf.registers[6],
                 dut.Decode.rf.registers[7],
                 dut.Decode.rf.registers[8],
                 dut.Decode.rf.registers[9],
                 dut.Decode.rf.registers[10],
                 dut.Decode.rf.registers[11],
                 dut.Memory.dmem.mem[0]);

`include "test_checks.vh"
        $finish;
    end

endmodule
