module total_module(Enable3, Enable6, Enable7, result, ready, sum, i, e, clk);
output reg[31:0] result;
output reg[31:0] ready;
output reg[31:0] sum;
output reg[31:0] i;
output reg[31:0] e;
input Enable3;
input Enable6;
input Enable7;
input clk;
always @(posedge clk) begin
if (Enable3) begin
sum = 0;
i = 0;
e = 20;
end
if (Enable6) begin
sum = sum + i;
i = i + 1;
end
if (Enable7) begin
result = sum;
ready = 1;
end
end
endmodule