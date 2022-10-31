library verilog;
use verilog.vl_types.all;
entity data_path is
    port(
        R3              : out    vl_logic_vector(31 downto 0);
        in1             : in     vl_logic_vector(31 downto 0);
        R4              : out    vl_logic_vector(31 downto 0);
        in2             : in     vl_logic_vector(31 downto 0);
        R               : out    vl_logic_vector(31 downto 0);
        S               : in     vl_logic_vector(31 downto 0);
        output2         : out    vl_logic_vector(31 downto 0);
        Enable3         : in     vl_logic;
        output5         : out    vl_logic_vector(31 downto 0);
        Enable7         : in     vl_logic;
        output8         : out    vl_logic_vector(31 downto 0);
        Enable9         : in     vl_logic;
        Enable10        : in     vl_logic;
        clk             : in     vl_logic
    );
end data_path;
