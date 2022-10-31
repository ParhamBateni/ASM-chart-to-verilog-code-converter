module TB;

reg clk, rst;
reg [31:0] S = 1;
wire [31:0] sum;
wire [31:0] ready, result;

main_program main_program1(S, ready, result, sum, clk, rst);

initial 
   begin
   clk = 0;
   rst = 0;
   #10
   rst = 1;
   #300
    $stop;
   end
   
always
  begin
   #5
   clk = ~clk;
  end
  
endmodule