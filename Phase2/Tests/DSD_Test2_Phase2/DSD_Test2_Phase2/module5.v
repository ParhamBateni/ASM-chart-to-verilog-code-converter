module module5(i, e, output5);
input [31:0] i;
input [31:0] e;
output reg [31:0] output5;
always @(i, e)
begin
if (i > e) begin
output5 = 1;
end else begin
output5 = 0; end
end
endmodule