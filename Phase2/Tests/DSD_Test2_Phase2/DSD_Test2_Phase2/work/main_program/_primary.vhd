library verilog;
use verilog.vl_types.all;
entity main_program is
    port(
        S               : in     vl_logic_vector(31 downto 0);
        ready           : out    vl_logic_vector(31 downto 0);
        result          : out    vl_logic_vector(31 downto 0);
        sum             : out    vl_logic_vector(31 downto 0);
        clk             : in     vl_logic;
        rst             : in     vl_logic
    );
end main_program;
