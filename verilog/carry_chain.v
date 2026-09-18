`timescale 1ns/1ps

// ----------------------------------------------------------------
// Cadena de N nucleos de carry local
// ----------------------------------------------------------------
module carry_chain
#(parameter W=32, parameter N=60)
(
    input  wire           clk,
    input  wire           rst,
    input  wire [W*N-1:0] A,
    input  wire [W*N-1:0] B,
    output wire [W*N-1:0] D,
    output wire [N-1:0]   done_vec,
    output wire           carry_out,
    output wire           all_done
);
    wire [N:0] fw;
    wire [N:0] fv;
    assign fw[0]=1'b0;
    assign fv[0]=1'b1;

    genvar gi;
    generate
        for(gi=0;gi<N;gi=gi+1) begin: GEN_CHAIN
            carry_nucleus #(.W(W)) u_n (
                .clk(clk), .rst(rst),
                .a_in(A[W*gi+:W]), .b_in(B[W*gi+:W]),
                .flag_in(fw[gi]),   .flag_valid(fv[gi]),
                .flag_out(fw[gi+1]),.flag_ready(fv[gi+1]),
                .d_out(D[W*gi+:W]), .done(done_vec[gi])
            );
        end
    endgenerate

    assign carry_out = fw[N];
    assign all_done  = &done_vec;
endmodule
