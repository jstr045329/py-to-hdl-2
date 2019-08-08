import random
from WhiteSpaceTools import eol, tab


# Choose which taps the reset signal is directly fed into:
direct_injection_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 100, 200, 300, 400, 450, 490]


def make_list(n, rand_seed=23487028):
    random.seed(rand_seed)
    assert(n >= 200)
    y = []
    for i in range(100, 100+n):
        y.append(i)
    random.shuffle(y)
    return y


def assign_fast_signals(format_str = "%04d", numel=200, num_drivers=3):
    assert(num_drivers >= 3)
    y = []
    for i in direct_injection_list:
        one_line = "sig_fast(" + (format_str % i) + ") <= reset_in"
        if i > 0:
            one_line += " or sig_fast(" + (format_str % (i-1)) + ")"
        if i > 20:
            one_line += " or sig_fast(" + (format_str % (i - 19)) + ")"
        if i >= 100:
            one_line += " or sig_fast(" + (format_str % (i - 81)) + ")"
        if i >= 200:
            one_line += " or sig_fast(" + (format_str % (i - 199)) + ")"
        one_line += ";"
        y.append(one_line)
    y.append("\n")
    mod_num = 0
    for i in range(numel):
        if i not in direct_injection_list:
            lower_bound = mod_num % 20
            mod_num += 1
            one_line = "sig_fast(" + (format_str % i) + ") <= sig_fast(" + \
                       (format_str % int(random.uniform(lower_bound, i))) + ")"

            for j in range(num_drivers-1):
                lower_bound = mod_num % 20
                mod_num += 1
                one_line += " or sig_fast(" + (format_str % int(random.uniform(lower_bound, i))) + ")"

            one_line += ";"
            y.append(one_line)
    return y


def assign_slow_signals(format_str = "%04d", numel=200, num_drivers=3):
    assert (num_drivers >= 3)
    y = []
    y.append("sig_slow(0) <= sig_fast(0);")
    mod_num = 0
    for i in range(1, numel):
        one_line = "sig_slow(" + (format_str % (i)) + ") <= sig_slow(" + (format_str % (i-1)) + ")"
        one_line += " or sig_fast(" + (format_str % (int(random.uniform(0, numel)))) + ")"
        lower_bound = mod_num % 20
        mod_num += 1
        for j in range(num_drivers):
            one_line += " or sig_slow(" + (format_str % int(random.uniform(lower_bound, i))) + ")"
        one_line += ";"
        y.append(one_line)
    return y


def assign_output(format_str = "%04d", numel=200, num_drivers=3):
    assert(num_drivers >= 3)
    y = []
    # Assign the output:
    y.append("reset_out <= sig_slow(0) or ")
    for i in range(10, numel+1):
        if i % 20 == 0:
            one_line = "             sig_slow(" + (format_str % (i-1)) + ")"
            if i < numel - 1:
                one_line += " or"
            else:
                one_line += ";"
            y.append(one_line)
    return y


def wrap_rst_mgr(numel=200, numdrivers=3):
    y = []
    y.append("library IEEE;")
    y.append("use IEEE.std_logic_1164.all;")
    y.append("")
    y.append("entity rst_mgr is")
    y.append("port(")
    y.append(tab() + "clock_fast  :  in  std_logic;")
    y.append(tab() + "clock_slow  :  in  std_logic;")
    y.append(tab() + "reset_in    :  in  std_logic;")
    y.append(tab() + "reset_out   : out  std_logic)")
    y.append("end rst_mgr;")
    y.append(eol())
    y.append("architecture rst_mgr_arch of rst_mgr is")
    y.append(tab() + "signal sig_fast : bit_vector(" + str(numel-1) + " downto 0);")
    y.append(tab() + "signal sig_slow : bit_vector(" + str(numel-1) + " downto 0);")
    y.append("begin")
    y.append(eol())

    # Create fast clock process:
    y.append("process(clock_fast)")
    y.append("begin")
    y.append(tab() + "if rising_edge(clock_fast) then")
    y.extend([tab(2) + i for i in assign_fast_signals(numel=numel, num_drivers=numdrivers)])
    y.append(tab() + "end if;")
    y.append("end process;")
    y.append(eol())

    # Create slow clock process:
    y.append("process(clock_slow)")
    y.append("begin")
    y.append(tab() + "if rising_edge(clock_slow) then")
    y.extend([tab(2) + i for i in assign_slow_signals(numel=numel, num_drivers=numdrivers)])
    y.append(tab() + "end if;")
    y.append("end process;")
    y.append(eol())
    y.extend(assign_output(numel=numel, num_drivers=numdrivers))
    y.append(eol())
    y.append("end rst_mgr_arch;")
    y.append(eol())
    return y


if __name__ == "__main__":
    with open("./vhdl_generated/reset_module.vhd", 'w') as f:
        for line in wrap_rst_mgr():
            f.write(line)
            f.write(eol())
