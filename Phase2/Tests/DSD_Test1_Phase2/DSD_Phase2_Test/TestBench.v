module TB;

reg clk, rst;
reg [31:0] in1 = 11;
reg [31:0] in2 = 13;
reg [31:0] S = 1;
wire [31:0] R4, R3, R;

main_program main_program1(in1, in2, S, R3, R4, R, clk, rst);

initial 
   begin
   clk = 0;
   rst = 0;
   #10
   rst = 1;
   #145
    $stop;
   end
   
always
  begin
   #5
   clk = ~clk;
  end
  
endmodule