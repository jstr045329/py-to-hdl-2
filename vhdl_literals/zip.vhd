-- ACTION: Come up with a way to make this work for N downto 0, 
-- but don't define N in the function. 
function zip_<my_type> (
        my_sig : in <my_type>;
        some_literal : in <my_type>)
        return <my_type> is
        variable i : integer;
        variable y : <my_type>;
begin 
        for i in 0 to my_sig'length-1 loop
                if i <= some_literal'length-1 then
                        y(i) <= some_literal(i);
                else
                        y(i) <= '0';
                end if;
        end loop;
        return y;
end;
