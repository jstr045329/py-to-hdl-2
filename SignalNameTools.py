"""Contains tools for generating signal names"""


def one_name(stub, revision, form, delay, format_str="%06d", is_input=False, is_output=False, is_var=False):
    if is_input:
        assert(not is_output)
        assert(not is_var)
    if is_output:
        assert(not is_input)
        assert(not is_var)
    if is_var:
        assert(not is_input)
        assert(not is_output)

    if is_output:
        suffix = "_o"
    elif is_input:
        suffix = "_i"
    elif is_var:
        suffix = "_v"
    else:
        suffix = "_s"
    return stub + "_r" + (format_str % revision) + "_f" + (format_str % form) + "_d" + (format_str % delay) + suffix


def is_int(one_char):
    try:
        int(one_char)
        return True
    except ValueError:
        return False


def extract_stub(s):
    """Extracts the name stub"""
    # todo: finish this
    pass


def extract_revision(s):
    """Extracts the revision number"""
    # todo: finish this
    pass


def extract_delay(s):
    """Extracts the delay number"""
    # todo: finish this
    pass


if __name__ == "__main__":
    print(one_name("my_sig", 42, 18, 299))
    print(one_name("my_sig", 42, 18, 299, is_input=True))
    print(one_name("my_sig", 42, 18, 299, is_output=True))
    print(one_name("my_var", 42, 18, 299, is_var=True))
    # print(is_int("_"))
    # print(is_int("3"))
