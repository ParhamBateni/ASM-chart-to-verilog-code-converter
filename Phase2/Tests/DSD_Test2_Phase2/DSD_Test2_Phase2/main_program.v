module main_program(S, ready, result, sum, clk, rst);
wire Enable3, Enable6, Enable7;
wire [31:0] output2, output5;
input clk, rst;
input [31:0] S;
output [31:0] ready;
output [31:0] result;
output [31:0] sum;
data_path dp(ready, S, result, sum, output2, Enable3, output5, Enable6, Enable7, clk);
control_unit cu(Enable3, Enable6, Enable7, output2, output5, clk, rst);
endmodule