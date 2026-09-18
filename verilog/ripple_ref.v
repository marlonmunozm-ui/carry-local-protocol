`timescale 1ns/1ps


module ripple_ref
#(parameter W=32, parameter N=60)
(
    input  wire           clk,
    input  wire           rst,
    input  wire [W*N-1:0] A,
    input  wire [W*N-1:0] B,
    output reg  [W*N-1:0] D,
    output reg            done,
    output reg  [7:0]     cycles_used
);
    reg [7:0] idx;
    reg       carry;
    reg [W:0] s;

    always @(posedge clk or posedge rst) begin
        if(rst) begin
            idx<=0; carry<=0; done<=0; D<=0; cycles_used<=0;
        end else if(!done) begin
            s = {1'b0,A[W*idx+:W]} + {1'b0,B[W*idx+:W]} + carry;
            D[W*idx+:W] <= s[W-1:0];
            carry        <= s[W];
            cycles_used  <= cycles_used + 1;
            if(idx==N-1) done<=1;
            else         idx<=idx+1;
        end
    end
endmodule
