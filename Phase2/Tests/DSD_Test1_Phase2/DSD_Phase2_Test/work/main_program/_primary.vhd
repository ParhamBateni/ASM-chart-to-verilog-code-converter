library verilog;
use verilog.vl_types.all;
entity main_program is
    port(
        in1             : in     vl_logic_vector(31 downto 0);
        in2             : in     vl_logic_vector(31 downto 0);
        S               : in     vl_logic_vector(31 downto 0);
        R3              : out    vl_logic_vector(31 downto 0);
        R4              : out    vl_logic_vector(31 downto 0);
        R               : out    vl_logic_vector(31 downto 0);
        clk             : in     vl_logic;
        rst             : in     vl_logic
    );
end main_program;
