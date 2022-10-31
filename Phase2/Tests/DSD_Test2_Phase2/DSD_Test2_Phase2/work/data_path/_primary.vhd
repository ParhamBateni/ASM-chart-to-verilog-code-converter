library verilog;
use verilog.vl_types.all;
entity data_path is
    port(
        ready           : out    vl_logic_vector(31 downto 0);
        S               : in     vl_logic_vector(31 downto 0);
        result          : out    vl_logic_vector(31 downto 0);
        sum             : out    vl_logic_vector(31 downto 0);
        output2         : out    vl_logic_vector(31 downto 0);
        Enable3         : in     vl_logic;
        output5         : out    vl_logic_vector(31 downto 0);
        Enable6         : in     vl_logic;
        Enable7         : in     vl_logic;
        clk             : in     vl_logic
    );
end data_path;
