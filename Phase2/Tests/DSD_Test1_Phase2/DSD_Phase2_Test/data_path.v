module data_path(R3, in1, R4, in2, R, S, output2, Enable3, output5, Enable7, output8, Enable9, Enable10, clk);
input Enable3, Enable7, Enable9, Enable10;
output [31:0] output2, output5, output8;
input clk;
input [31:0] in1;
input [31:0] in2;
input [31:0] S;
output [31:0] R3;
output [31:0] R4;
output [31:0] R;
wire [31:0] R1;
wire [31:0] R2;
module2 create_module2(S, output2);
module5 create_module5(R1, R2, output5);
module8 create_module8(R1, output8);
total_module total_module1(Enable3, Enable7, Enable9, Enable10, R3, in1, R4, R1, in2, R, R2, clk);
endmodule