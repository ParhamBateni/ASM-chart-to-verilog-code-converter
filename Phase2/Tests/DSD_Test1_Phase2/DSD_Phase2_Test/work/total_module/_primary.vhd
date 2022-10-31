library verilog;
use verilog.vl_types.all;
entity total_module is
    port(
        Enable3         : in     vl_logic;
        Enable7         : in     vl_logic;
        Enable9         : in     vl_logic;
        Enable10        : in     vl_logic;
        R3              : out    vl_logic_vector(31 downto 0);
        in1             : in     vl_logic_vector(31 downto 0);
        R4              : out    vl_logic_vector(31 downto 0);
        R1              : out    vl_logic_vector(31 downto 0);
        in2             : in     vl_logic_vector(31 downto 0);
        R               : out    vl_logic_vector(31 downto 0);
        R2              : out    vl_logic_vector(31 downto 0);
        clk             : in     vl_logic
    );
end total_module;
