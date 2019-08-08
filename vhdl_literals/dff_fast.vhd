library IEEE;
use IEEE.std_logic_1164.all;

entity dff is 
        generic(width : integer);
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
