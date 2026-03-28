`ifndef SIGN_EXTEND_V
`define SIGN_EXTEND_V

module Sign_Extend(In, Imm_Ext, ImmSrc);

    input [31:0] In;
    input [1:0] ImmSrc;
    output [31:0] Imm_Ext;
    reg [31:0] Imm_Ext;

    always @(*) begin
        case (ImmSrc)
            2'b00: Imm_Ext = {{20{In[31]}}, In[31:20]};
            2'b01: Imm_Ext = {{20{In[31]}}, In[31:25], In[11:7]};
            2'b10: Imm_Ext = {{19{In[31]}}, In[31], In[7], In[30:25], In[11:8], 1'b0};
            2'b11: Imm_Ext = {{11{In[31]}}, In[31], In[19:12], In[20], In[30:21], 1'b0};
            default: Imm_Ext = 32'h00000000;
        endcase
    end

endmodule

`endif
