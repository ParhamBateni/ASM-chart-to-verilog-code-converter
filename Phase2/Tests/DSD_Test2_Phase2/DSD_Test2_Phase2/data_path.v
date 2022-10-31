module data_path(ready, S, result, sum, output2, Enable3, output5, Enable6, Enable7, clk);
input Enable3, Enable6, Enable7;
output [31:0] output2, output5;
input clk;
input [31:0] S;
output [31:0] ready;
output [31:0] result;
output [31:0] sum;
wire [31:0] i;
wire [31:0] e;
module2 create_module2(S, output2);
module5 create_module5(i, e, output5);
total_module total_module1(Enable3, Enable6, Enable7, result, ready, sum, i, e, clk);
endmodule