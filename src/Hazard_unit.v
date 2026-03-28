`ifndef HAZARD_UNIT_V
`define HAZARD_UNIT_V

module hazard_unit(rst, PCSrcE, RegWriteM, RegWriteW, ResultSrcE, ResultSrcM, UseRs1D, UseRs2D, RD_E, RD_M, RD_W, Rs1_D, Rs2_D, Rs1_E, Rs2_E, StallF, StallD, FlushD, FlushE, ForwardAE, ForwardBE);

    input rst, PCSrcE, RegWriteM, RegWriteW;
    input UseRs1D, UseRs2D;
    input [1:0] ResultSrcE, ResultSrcM;
    input [4:0] RD_E, RD_M, RD_W, Rs1_D, Rs2_D, Rs1_E, Rs2_E;
    output StallF, StallD, FlushD, FlushE;
    output [1:0] ForwardAE, ForwardBE;

    wire LoadUseStallD;
    wire ForwardFromM_A;
    wire ForwardFromM_B;
    wire ForwardFromW_A;
    wire ForwardFromW_B;

    assign LoadUseStallD = rst &&
                           (ResultSrcE == 2'b01) &&
                           (RD_E != 5'd0) &&
                           ((UseRs1D && (RD_E == Rs1_D)) || (UseRs2D && (RD_E == Rs2_D)));

    assign StallF = LoadUseStallD;
    assign StallD = LoadUseStallD;
    assign FlushD = PCSrcE;
    assign FlushE = PCSrcE || LoadUseStallD;

    assign ForwardFromM_A = rst &&
                            RegWriteM &&
                            (ResultSrcM != 2'b01) &&
                            (RD_M != 5'd0) &&
                            (RD_M == Rs1_E);
    assign ForwardFromM_B = rst &&
                            RegWriteM &&
                            (ResultSrcM != 2'b01) &&
                            (RD_M != 5'd0) &&
                            (RD_M == Rs2_E);
    assign ForwardFromW_A = rst &&
                            RegWriteW &&
                            (RD_W != 5'd0) &&
                            (RD_W == Rs1_E) &&
                            !ForwardFromM_A;
    assign ForwardFromW_B = rst &&
                            RegWriteW &&
                            (RD_W != 5'd0) &&
                            (RD_W == Rs2_E) &&
                            !ForwardFromM_B;

    assign ForwardAE = ForwardFromM_A ? 2'b10 :
                       ForwardFromW_A ? 2'b01 :
                       2'b00;

    assign ForwardBE = ForwardFromM_B ? 2'b10 :
                       ForwardFromW_B ? 2'b01 :
                       2'b00;

    // Separate instruction and data memories avoid classic IF/MEM structural hazards.

endmodule

`endif
