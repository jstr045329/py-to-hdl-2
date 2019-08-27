"""Contains tools for generating Finite State Machines (FSMs)"""
import sys
sys.path.append("..")
from dec2bin import dec2bin
from is_int import is_int
from math import ceil, log 


def extract_inputs(condition):
    """Extracts the inputs from a condition. For example:
            a and b or c
       will return:
            ['a', 'b', 'c']"""
    y = set()
    condition = condition.replace("!", " ")
    condition = condition.replace(" and ", " ")
    condition = condition.replace(" or ", " ")
    condition = condition.replace(" xor ", " ")
    condition = condition.replace(" nand ", " ")
    condition = condition.replace(" not ", " ")
    condition = condition.replace(" nor ", " ")
    condition = condition.replace(" xnor ", " ")
    condition = condition.replace("(", " ")
    condition = condition.replace(")", " ")
    los = condition.split()
    for one_tok in los:
        if not is_int(one_tok):
            y.add(one_tok)
    return y 


def extract_one_output(some_result):
    if not isinstance(some_result, str):
        return None
    stop_idx = some_result.find("<=")
    if stop_idx == -1:
        return None
    raw_output = some_result[:stop_idx]
    clean_output = raw_output.split()
    return clean_output[0]


class FsmGenerator:
    def __init__(self):
        self.default_state = "reset"
        self.states = set()
        self.edges = []
        self.inputs = set()
        self.outputs = set()
        self.physical_expressions = set()
        self.state_to_phys = []
        self.input_to_width = {}
        self.output_to_width = {}
        self.edge_to_output = []            # Maps Edges to output effects

    def add_state(self, new_state, physical_expression=None):
        """If physical_expression is None, a rendering function will map states to physical values
        however it wants."""
        self.states.add(new_state)
        self.physical_expressions.add(physical_expressions)
        self.state_to_phys.append((new_state, physical_expression))
        if None in self.physical_expressions:
            # If you pass in None for 1 physical expression, you must pass in None
            # for all of them. Therefore, the size of this set should be 1.
            assert(len(self.physical_expressions) == 1)
        else:
            # If you specify physical expressions, the set of physical expressions should be 
            # the same size as the set of states. 
            assert(len(self.physical_expressions) == len(self.states))

    def add_edge(self, from_state, to_state, condition, result_list=[]):
        assert(from_state in self.state_list)
        assert(to_state in self.state_list)
        self.edges.append((from_state, to_state, condition, result_list))
        for one_input in extract_inputs(condition):
            self.inputs.add(one_input)
        for one_result in result_list:
            self.outputs.add(extract_one_output(one_result))
        # todo: Extract values against which inputs are being compared
        # todo: See if we can make any inferences about the sizes of outputs
        # todo: Update input_to_width and output_to_width accordingly. 
        # todo: Update edge_to_output, so that effects of state transitions on outputs can
        #       be assigned
        
    def render_vhdl(self):
        state_list = list(self.states)
        state_list.sort()
        input_list = list(self.inputs)
        input_list.sort()
        output_list = list(self.outputs)
        output_list.sort()
        if None in self.physical_expressions:
            # In this case, physical expressions have not been defined, so define them linearly:
            state_to_phys = []
            bits_required = ceil(log(len(state_list), 2))
            for m in range(len(state_list)):
                state_to_phys.append((state_list[m], bin2dec(m, bits_required)))
            self.state_to_phys = state_to_phys
        else:
            bits_required = ceil(log(len(self.state_to_phys), 2))

        msb_name = str(bits_required - 1)
        bit_range = "(" + msb_name + " downto 0)"

        const_list = []
        for one_state, phys_expr in self.state_to_phys:
            one_str = "constant " + one_state + " : std_logic_vector" + bit_range + " := " + phys_expr + ";"
            const_list.append(one_str)
        
        # Generate lists for declaring signals, inputs, outputs, etc:
        sig_dec_list = []
        sig_dec_list.append("signal state : std_logic_vector" + bit_range + " := (others => '0');")


def test_fsm_generator():
    uut = FsmGenerator()
    for m in range(10):
        uut.add_state("state_%04d" % m)
#    uut.add_edge("state_01", "state_02")


if __name__ == "__main__":
    test_fsm_generator()































