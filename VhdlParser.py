"""Contains a tool for extracting the interface from a VHDL entity."""
chars_to_pad = ["(", ")", ";", "<=", ":="]


def guarantee_whitespace(s):
    for one_char in chars_to_pad:
        s = s.replace(one_char, " " + one_char + " ")
    return s


def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def make_one_port(name, dir, dtype, width):
    # assert(dir == "in" or dir == "out" or dir == "inout")
    return {
        "name": name,
        "direction": dir,
        "datatype": dtype,
        "width": width,
        "is_port": True,
        "is_generic": False
    }


def make_one_generic(name, dtype, width):
    assert(dir == "in" or dir == "out" or dir == "inout")
    return {
        "name": name,
        "direction": "in",
        "datatype": dtype,
        "width": width,
        "is_port": False,
        "is_generic": True
    }


# LOOKING_FOR_ENTITY_DECLARATION = "LOOKING_FOR_ENTITY_DECLARATION"
# FOUND_ENTITY = "FOUND_ENTITY"
# EATING_GENERICS = "EATING_GENERICS"
# EATING_PORTS = "EATING_PORTS"


def scan_one_file(filename):
    with open(filename, 'r') as f:
        bigstr = f.read()
        bigstr = guarantee_whitespace(bigstr)
        los = bigstr.split()
        ports = []
        generics = []
        # for one_tok in los:
        for i in range(len(los)):
            one_tok = los[i]
            if one_tok == "port":
                short_list = los[i:]
                paren_depth = 0
                state = 0
                prev_state = 0
                prev_paren_depth = 0
                new_port = None
                enable_width_detection = True
                for shrt_token in short_list:
                    if shrt_token == "(":
                        paren_depth += 1
                    elif shrt_token == ")":
                        paren_depth -= 1
                    elif shrt_token == ";":
                        state = 0
                        this_name = "reset name"
                        this_width = "1"
                        this_direction = "reset dir"
                        this_type = "reset type"
                        enable_width_detection = True
                    elif shrt_token == ":":
                        state = 1
                    elif shrt_token == ":=":
                        state = 200
                    elif shrt_token == "downto":
                        state = 100
                    else:
                        if state == 0:
                            this_name = shrt_token
                        elif state == 1:
                            this_direction = shrt_token
                            state = 2
                        elif state == 2:
                            this_type = shrt_token
                            new_port = make_one_port(this_name, this_direction, this_type, "1")
                            ports.append(new_port)
                            state = 3
                        elif state == 3:
                            if enable_width_detection:
                                this_width = shrt_token
                                if is_int(this_width):
                                    this_width = str(int(this_width) + 1)
                                enable_width_detection = False
                                new_port["width"] = this_width
                    # if (state == 0 and prev_state != 0) or (paren_depth == -1):
                    if paren_depth == -1:
                        break

                    prev_state = state
                    prev_paren_depth = paren_depth



            elif one_tok == "port":
                short_list = los[i:]

    return ports




if __name__ == "__main__":
    for one_port in scan_one_file("./vhdl_literals/dff_fast.vhd"):
        print(str(one_port))





