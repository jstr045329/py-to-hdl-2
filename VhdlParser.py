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


def make_one_port(name, dir, dtype):
    assert(dir == "in" or dir == "out" or dir == "inout")
    return {
        "name": name,
        "direction": dir,
        "datatype": dtype,
        "width": "1",
        "default_value": "",
        "is_port": True,
        "is_generic": False,
    }


def make_one_generic(name, dtype):
    return {
        "name": name,
        "direction": "in",
        "datatype": dtype,
        "width": "1",
        "default_value": "",
        "is_port": False,
        "is_generic": True,
    }


def extract_ports(short_list):
    ports = []
    paren_depth = 0
    state = 0
    state_history = [0] * 100
    paren_depth_history = [0] * 100
    new_port = None
    enable_width_detection = True
    enable_default_value_detection = True
    this_default = ""
    require_more_tokens = False
    num_tokens_counted = 0
    for shrt_token in short_list:
        # print("token:", shrt_token, "       depth: ", paren_depth)
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
            this_default = ""
            enable_width_detection = True
            enable_default_value_detection = True
            require_more_tokens = False
            num_tokens_counted = 0
        elif shrt_token == ":":
            state = 1
        elif shrt_token == "downto":
            state = 100
        elif shrt_token == ":=":
            state = 200
        else:
            if state == 0:
                this_name = shrt_token
            elif state == 1:
                this_direction = shrt_token
                state = 2
            elif state == 2:
                this_type = shrt_token
                new_port = make_one_port(this_name, this_direction, this_type)
                ports.append(new_port)
                state = 3
            elif state == 3:
                if enable_width_detection:
                    this_width = shrt_token
                    if is_int(this_width):
                        this_width = str(int(this_width) + 1)
                    enable_width_detection = False
                    new_port["width"] = this_width
            elif state == 100:
                pass
            elif state == 200:
                if enable_default_value_detection:
                    num_tokens_counted = 0
                    this_default = shrt_token
                    if shrt_token == "others":
                        require_more_tokens = True
                    else:
                        require_more_tokens = False
                    enable_default_value_detection = False
                    new_port["default_value"] = this_default
                elif require_more_tokens:
                    if num_tokens_counted < 3:
                        new_port["default_value"] += shrt_token

        if shrt_token == ";" and paren_depth == 0:
            break

        state_history.append(state)
        paren_depth_history.append(paren_depth)
    return ports


def extract_generics(short_list):
    generics = []
    paren_depth = 0
    state = 0
    state_history = [0] * 100
    paren_depth_history = [0] * 100
    new_port = None
    enable_width_detection = True
    enable_default_value_detection = True
    this_default = ""
    require_more_tokens = False
    num_tokens_counted = 0
    for shrt_token in short_list:
        # print("token:", shrt_token, "       depth: ", paren_depth)
        if shrt_token == "(":
            paren_depth += 1
        elif shrt_token == ")":
            paren_depth -= 1
        elif shrt_token == ";":
            state = 0
            this_name = "reset name"
            this_width = "1"
            this_type = "reset type"
            this_default = ""
            enable_width_detection = True
            enable_default_value_detection = True
            require_more_tokens = False
            num_tokens_counted = 0
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
                this_type = shrt_token
                new_generic = make_one_generic(this_name, this_type)
                generics.append(new_generic)
                state = 3
            elif state == 3:
                if enable_width_detection:
                    this_width = shrt_token
                    if is_int(this_width):
                        this_width = str(int(this_width) + 1)
                    enable_width_detection = False
                    new_generic["width"] = this_width
            elif state == 100:
                pass
            elif state == 200:
                if enable_default_value_detection:
                    num_tokens_counted = 0
                    this_default = shrt_token
                    if shrt_token == "others":
                        require_more_tokens = True
                    else:
                        require_more_tokens = False
                    enable_default_value_detection = False
                    new_generic["default_value"] = this_default
                elif require_more_tokens:
                    if num_tokens_counted < 3:
                        new_generic["default_value"] += shrt_token

        if shrt_token == ";" and paren_depth == 0:
            break

        state_history.append(state)
        paren_depth_history.append(paren_depth)
    return generics


def scan_one_file(filename):
    with open(filename, 'r') as f:
        bigstr = f.read()
        bigstr = guarantee_whitespace(bigstr)
        los = bigstr.split()
        ent_list = []
        port_dictionary = {}
        generic_dictionary = {}
        for i in range(len(los)):
            one_tok = los[i]
            # print(one_tok)
            if one_tok == "entity":
                module_name = los[i+1]
                ent_list.append(module_name)
            elif one_tok == "port":
                port_dictionary[module_name] = extract_ports(los[i:])
            elif one_tok == "generic":
                generic_dictionary[module_name] = extract_generics(los[i:])
    return ent_list, port_dictionary, generic_dictionary

# todo: Extend this to capture multiple entities in the same file

if __name__ == "__main__":
    nd, pd, gd = scan_one_file("./vhdl_literals/vhd_test.vhd")
    # print(nd)
    for one_entity in nd:
        print("module name:     ", one_entity)
        g = gd[one_entity]
        p = pd[one_entity]
        for one_generic in g:
            print(str(one_generic))
        for one_port in p:
            print(str(one_port))
        print("\n"*6)





