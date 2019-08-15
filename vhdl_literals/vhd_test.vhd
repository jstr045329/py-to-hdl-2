library IEEE;
use IEEE.std_logic_1164.all;

entity dff is
        generic(
              x : integer;
              width : integer := 42;
              some_val : std_logic_vector(99 downto 0);
              val02 : bit_vector(0 downto 0) := X"0000039FCA0000000001" );
        port(
              clk   :   in    bit_vector(0 downto 0);
              d     :   in    bit_vector(width-1 downto 0);
              en    :   in    bit_vector(0 downto 0) := (others => '0');
              q     :   out   bit_vector(width-1 downto 0));
end dff;

architecture dff_arch of dff is
        signal q0 : bit_vector(width-1 downto 0) := (others => '0');
begin

process(clk)
begin
        if rising_edge(clk(0)) then
                if en(0) = '1' then
                        q0 <= d;
                end if;
        end if;
end process;

q <= q0;

end dff_arch;

entity dff2 is
        generic(
              xyzcal : whatever_type;
              width : integer := 42;
              some_val : std_logic_vector(99 downto 0);
              val02 : bit_vector(0 downto 0) := X"0000039FCA0000000001" );
        port(
              clk   :   in    bit_vector(0 downto 0);
              d     :   in    bit_vector(width-1 downto 0);
              en    :   in    bit_vector(0 downto 0) := (others => '0');
              q     :   out   bit_vector(width-1 downto 0));
end dff;

entity dff3 is
        generic(
              x : integer;
              width : integer := 42;
              some_val : std_logic_vector(99 downto 0);
              my_generic_name : bit_vector(0 downto 0) := X"0000039FCA0000000001" );
        port(
              clk   :   in    bit_vector(0 downto 0);
              d     :   in    bit_vector(width-1 downto 0);
              en0042  :   inout    bit_vector(0 downto 0) := (others => '0');
              q4300 :   out   bit_vector(width-1 downto 0));
end dff;
