library verilog;
use verilog.vl_types.all;
entity control_unit is
    port(
        Enable3         : out    vl_logic;
        Enable7         : out    vl_logic;
        Enable9         : out    vl_logic;
        Enable10        : out    vl_logic;
        output2         : in     vl_logic_vector(31 downto 0);
        output5         : in     vl_logic_vector(31 downto 0);
        output8         : in     vl_logic_vector(31 downto 0);
        clk             : in     vl_logic;
        rst             : in     vl_logic
    );
end control_unit;
