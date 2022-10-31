module module5(R1, R2, output5);
input [31:0] R1;
input [31:0] R2;
output reg [31:0] output5;
always @(R1, R2)
begin
if (R1 < R2) begin
output5 = 1;
end else begin
output5 = 0; end
end
endmodule