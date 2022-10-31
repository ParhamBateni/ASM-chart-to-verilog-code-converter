module total_module(Enable3, Enable7, Enable9, Enable10, R3, in1, R4, R1, in2, R, R2, clk);
output reg[31:0] R3;
output reg[31:0] R4;
output reg[31:0] R1;
output reg[31:0] R;
output reg[31:0] R2;
input [31:0] in1;
input [31:0] in2;
input Enable3;
input Enable7;
input Enable9;
input Enable10;
input clk;
always @(posedge clk) begin
if (Enable3) begin
R1 = in1;
R2 = in2;
R3 = 0;
R = 0;
end
if (Enable7) begin
R2 = R1;
R1 = R2;
end
if (Enable9) begin
R4 = R3;
R = 1;
end
if (Enable10) begin
R3 = R3 + R2;
R1 = R1 - 1;
end
end
endmodule