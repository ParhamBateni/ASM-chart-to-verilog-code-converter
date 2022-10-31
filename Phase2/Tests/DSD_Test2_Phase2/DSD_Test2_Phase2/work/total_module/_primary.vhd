library verilog;
use verilog.vl_types.all;
entity total_module is
    port(
        Enable3         : in     vl_logic;
        Enable6         : in     vl_logic;
        Enable7         : in     vl_logic;
        result          : out    vl_logic_vector(31 downto 0);
        ready           : out    vl_logic_vector(31 downto 0);
        sum             : out    vl_logic_vector(31 downto 0);
        i               : out    vl_logic_vector(31 downto 0);
        e               : out    vl_logic_vector(31 downto 0);
        clk             : in     vl_logic
    );
end total_module;
