module main_program(in1, in2, S, R3, R4, R, clk, rst);
wire Enable3, Enable7, Enable9, Enable10;
wire [31:0] output2, output5, output8;
input clk, rst;
input [31:0] in1;
input [31:0] in2;
input [31:0] S;
output [31:0] R3;
output [31:0] R4;
output [31:0] R;
data_path dp(R3, in1, R4, in2, R, S, output2, Enable3, output5, Enable7, output8, Enable9, Enable10, clk);
control_unit cu(Enable3, Enable7, Enable9, Enable10, output2, output5, output8, clk, rst);
endmodule