module module2(S, output2);
input [31:0] S;
output reg [31:0] output2;
always @(S)
begin
if (S == 1) begin
output2 = 1;
end else begin
output2 = 0; end
end
endmodule