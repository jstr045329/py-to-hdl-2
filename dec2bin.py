"""Contains a tool for converting decimal numbers to binary strings"""


def dec2bin(x, num_dig, wrap_in_quotes=True):
    s = bin(x)
    s = s.replace("0b", "")
    assert(num_dig >= len(s))
    if len(s) < num_dig:
        num_zeros = num_dig - len(s)
        s = "0" * num_zeros + s
    if wrap_in_quotes:
        return '"' + s + '"'
    return s


def test_dec2bin():
    x = dec2bin(8, 12, False)
    assert(x == "000000001000")
    x = dec2bin(13, 16, False)
    assert(x == "0000000000001101")
    x = dec2bin(255, 24, False)
    assert(x == "000000000000000011111111")
    x = dec2bin(255, 24, True)
    assert(x == '"000000000000000011111111"')

