`timescale 1ns/1ps

// ================================================================
// Modelo de Carry Local
// ================================================================
module carry_nucleus
#(parameter W = 32)
(
    input  wire         clk,
    input  wire         rst,
    input  wire [W-1:0] a_in,
    input  wire [W-1:0] b_in,
    input  wire         flag_in,
    input  wire         flag_valid,
    output reg          flag_out,
    output reg          flag_ready,
    output reg  [W-1:0] d_out,
    output reg          done
);
    wire [W:0] sum        = {1'b0,a_in} + {1'b0,b_in};
    wire       is_gen     = sum[W];
    wire       is_front   = (~sum[W]) & (&sum[W-1:0]);

    localparam ST_IDLE=2'd0, ST_COMP=2'd1, ST_WAIT=2'd2, ST_DONE=2'd3;
    reg [1:0] st;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            st<=ST_IDLE; d_out<=0; flag_out<=0; flag_ready<=0; done<=0;
        end else begin
            case(st)
                ST_IDLE: begin
                    done<=0; flag_ready<=0;
                    if(is_gen) begin
                        d_out<=sum[W-1:0]; flag_out<=1; flag_ready<=1; st<=ST_COMP;
                    end else if(!is_front) begin
                        d_out<=sum[W-1:0]; flag_out<=0; flag_ready<=1; st<=ST_COMP;
                    end else begin
                        d_out<=sum[W-1:0]; st<=ST_WAIT;
                    end
                end
                ST_COMP: begin
                    if(flag_valid) begin
                        if(flag_in) begin
                            if(&d_out) begin d_out<=0; flag_out<=1; end
                            else       begin d_out<=d_out+1; flag_out<=0; end
                        end
                        flag_ready<=1; done<=1; st<=ST_DONE;
                    end
                end
                ST_WAIT: begin
                    if(flag_valid) begin
                        if(flag_in) begin d_out<=0; flag_out<=1; end
                        else        begin             flag_out<=0; end
                        flag_ready<=1; done<=1; st<=ST_DONE;
                    end
                end
                ST_DONE: done<=1;
            endcase
        end
    end
endmodule
