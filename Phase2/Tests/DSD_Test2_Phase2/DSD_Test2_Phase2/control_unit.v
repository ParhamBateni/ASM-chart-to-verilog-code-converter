module control_unit(Enable3, Enable6, Enable7, output2, output5, clk, rst);
input [31:0] output2, output5;
output reg Enable3, Enable6, Enable7;
input clk, rst;
integer p_state, n_state;

always @ (posedge clk)
begin
if (rst == 1'b0) begin p_state = 1; end
else begin p_state = n_state; end
end

always @(p_state, output2, output5)
begin
begin
Enable3 = 0;
Enable6 = 0;
Enable7 = 0;
end
case(p_state)
1:
begin
if (output2 == 1) begin
begin Enable3 = 1; end
begin n_state = 4; end
end else begin
begin n_state = 1; end
end
end
4:
begin
if (output5 == 1) begin
begin Enable7 = 1; end
begin n_state = 1; end
end else begin
begin Enable6 = 1; end
begin n_state = 4; end
end
end
endcase
end
endmodule