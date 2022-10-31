module module8(R1, output8);
input [31:0] R1;
output reg [31:0] output8;
always @(R1)
begin
if (R1 == 0) begin
output8 = 1;
end else begin
output8 = 0; end
end
endmodule