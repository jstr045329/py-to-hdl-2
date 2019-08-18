from copy import deepcopy
from EngineeringUnits import Inf
from ParseExpression import parse_expression
from Signal import Signal
from ValidateMode import validate_mode
from WhiteSpaceTools import eol, tab


def validate_default_datatype(s):
    assert(s == "bit" or s == "std_logic" or s == "std_ulogic")


DEFAULT_GLOBAL_RESET_NAME = "rst_global"


synthesizable_types = ["bit", "std_logic", "std_ulogic"]


class Entity:
    def __init__(self, nm, **kwargs):
        """If you include the default_bit_value keyword argument, you must
        wrap the value in any necessary quotes."""
        self.module_name = nm
        self.signals = set()
        self.components = set()
        self.port_maps = []
        self.clocks = set()
        self.resets = set()
        if "global_rst" in kwargs:
            self.resets.add(kwargs["global_rst"])
            self.global_rst = kwargs["global_rst"]
        else:
            self.resets.add(DEFAULT_GLOBAL_RESET_NAME)
            self.global_rst = DEFAULT_GLOBAL_RESET_NAME

        if "default_clk" in kwargs:
            self.default_clk = kwargs["default_clk"]
        else:
            self.default_clk = "clk"
        self.clocks.add(self.default_clk)
        self.inputs = set()
        self.inputs_used = set()
        self.outputs = set()
        self.outputs_used = set()
        self.signals = set()
        self.signals_assigned = set()
        self.signals_used = set()
        self.generics = set()
        self.generics_assigned = set()
        self.generics_used = set()
        self.components = set()
        self.child_modules = set()
        self.expressions_by_name = {}       # Maps signal/output names to assignment expressions
        self.clocks_by_name = {}            # Maps signa/output names to the clocks with which they should be sync'd
        self.names_by_clock = {}            # Maps clocks to signal/output names
        self.child_instances = []
        self.shell_script = []
        self.tcl_script = []
        self.double_buffer_inputs = False
        self.render_global_reset = True
        self.route_clks_through_high_fanout = False
        self.disable_clk_rendering = False
        self.disable_global_reset_rendering = False     # Set to true for purely combinational modules.
        self.is_synchronous = True
        self.speed_mode = "fast"
        validate_mode(self.speed_mode)                  # A call to validate_speed_mode() should always follow an
                                                        # assignment to self.speed_mode.

        self.called_validation_method = False           # todo: Enforce validation call before rendering
        self.inherit_parent_datatypes = True            # Will inherit bit/vector, std_logic/vector, etc. from parent.
        if "default_datatype" in kwargs:
            self.default_datatype = kwargs["default_datatype"]
            validate_default_datatype(self.default_datatype)
        else:
            self.default_datatype = "bit"
            validate_default_datatype(self.default_datatype)
        if "default_bit_value" in kwargs:
            # Note: You must include any ''
            self.default_bit_value = kwargs["default_bit_value"]
        else:
            self.default_bit_value = "'0'"
        self.instantiate_rst_module = False
        self.parent = None
        self.favor_fast_sim = False
        self.fast_datatype = "bit"
        self.accurate_datatype = "std_logic"

    def set_as_top_level(self):
        self.double_buffer_inputs = True
        self.instantiate_rst_module = True
        self.route_clks_through_high_fanout = True

    def add_module(self, c, inherit=True):
        self.child_modules.add(c)
        if inherit:
            c.accurate_datatype = self.accurate_datatype
            c.fast_datatype = self.fast_datatype
            c.favor_fast_sim = self.favor_fast_sim

    def instantiate_child(self, one_portmap):
        """Pass in the port map through kwargs"""
        # todo: finish this
        pass

    def set_as_unclocked(self):
        self.disable_clk_rendering = True
        self.is_synchronous = False

    def add_clk(self, nm):
        self.clocks.add(nm)

    def add_generic(self, nm, **kwargs):
        y = Signal(nm, **kwargs)
        self.generics.add(y)

    def add_input(self, nm, **kwargs):
        y = Signal(nm, **kwargs)
        self.inputs.add(y)

    def add_signal(self, nm, **kwargs):
        """_s will be appended to whatever name you pass in"""
        name = nm + "_s"
        y = Signal(name, **kwargs)
        self.signals.add(y)
        if "expr" in kwargs:
            if "raw_vhd" in kwargs and kwargs["raw_vhd"]:
                # In this case, write the VHDL expression directly:
                self.expressions_by_name[name] = kwargs["expr"]
            else:
                # In this case, regard expr as a C-like expression:
                self.expressions_by_name[name] = parse_expression(kwargs["expr"])
        else:
            self.expressions_by_name[name] = " (others => '0');  -- TODO: Fill this in"

        if "clk" in kwargs:
            self.clocks_by_name[name] = kwargs["clk"]
        else:
            if not self.disable_clk_rendering:
                self.clocks_by_name[name] = self.default_clk

    def add_output(self, nm, **kwargs):
        """This will create a signal ending in _s and an output ending in _o, drive the signal with the
        expression, and drive the """
        y0 = Signal(nm + "_s", **kwargs)
        y1 = Signal(nm + "_o", **kwargs)
        self.signals.add(y0)
        self.outputs.add(y1)
        if "clk" in kwargs:
            self.clocks_by_name[nm + "_s"] = kwargs["clk"]
        else:
            if self.disable_clk_rendering:
                pass
            else:
                self.clocks_by_name[nm + "_s"] = self.default_clk
        self.clocks_by_name[nm + "_o"] = "__async__"
        self.expressions_by_name[nm + "_s"] = " (others => '0')"  # todo: somehow put a useful expression in here
        self.expressions_by_name[nm + "_o"] = nm + "_s"

        # todo: Get rid of everything in Signal.py that should not be done at the signal level

    def render_component_declaration_vhdl(self):
        if self.favor_fast_sim:
            the_datatype = self.fast_datatype
        else:
            the_datatype = self.accurate_datatype
        y = []
        y.append("component " + self.module_name + " is")
        i = 0
        if len(self.generics) > 0:
            y.append(tab() + "generic(")
            for one_generic in self.generics:
                one_str = tab(2) + one_generic.name + " : " + one_generic.datatype
                one_str += ("_vector(" + str(one_generic.width-1) + " downto 0)") if \
                (one_generic.datatype in synthesizable_types) else ""
                one_str += ";" if i < len(self.generics) - 1 else ");"
                y.append(one_str)
                i += 1

        y.append(tab() + "port(")
        i = 0
        for one_input in self.inputs:
            one_str = tab(2) + one_input.name + " :  in " + the_datatype + "_vector(" + \
                      str(one_input.width-1) + " downto 0);"
            y.append(one_str)
            i += 1

        i = 0
        for one_output in self.outputs:
            one_str = tab(2) + one_output.name + " : out " + the_datatype + "_vector(" + \
                      str(one_input.width - 1) + " downto 0)"
            one_str += ";" if i < len(self.inputs) - 1 else ");"
            y.append(one_str)
            i += 1
        y.append("end component;")
        return y

    def render_component_declaration_verilog(self):
        pass

    def render_port_map_vhdl(self):
        raise NotImplemented()

    def render_port_map_verilog(self):
        raise NotImplemented()

    def render_module_vhdl(self):
        """Includes entity declaration"""
        if self.favor_fast_sim:
            the_datatype = self.fast_datatype
        else:
            the_datatype = self.accurate_datatype
        y = []
        y.append(eol())
        y.append("library IEEE;")
        y.append("use IEEE.std_logic_1164.all;")
        y.append(eol())
        y.append("entity " + self.module_name + " is")

        i = 0
        if len(self.generics) > 0:
            y.append(tab() + "generic(")
            for one_generic in self.generics:
                one_str = tab(2) + one_generic.name + " : " + one_generic.datatype
                one_str += ("_vector(" + str(one_generic.width-1) + " downto 0)") if \
                (one_generic.datatype in synthesizable_types) else ""
                one_str += ";" if i < len(self.generics) - 1 else ");"
                y.append(one_str)
                i += 1

        y.append(tab() + "port(")
        for one_input in self.inputs:
            one_str = tab(2) + one_input.name + " :  in " + the_datatype + "_vector(" + \
                      str(one_input.width-1) + " downto 0);"
            # one_str += ";" if i < len(self.inputs)-1 else ");"
            y.append(one_str)
            i += 1

        i = 0
        for one_output in self.outputs:
            one_str = tab(2) + one_output.name + " : out " + the_datatype + "_vector(" + \
                      str(one_input.width - 1) + " downto 0)"
            one_str += ";" if i < len(self.inputs) - 1 else ");"
            y.append(one_str)
            i += 1

        y.append("end " + self.module_name + ";")
        y.append(eol())
        y.append("architecture " + self.module_name + "_arch of " + self.module_name + " is" )

        for one_child in self.child_modules:
            y.extend([tab() + i for i in one_child.render_component_declaration_vhdl()])
            y.append(eol())
        for one_signal in self.signals:
            y.append(tab() + "signal    " + one_signal.name + "   :   " + the_datatype +
                     "_vector(" + str(one_signal.width-1) + " downto 0);")
        y.append(eol())
        y.append("begin")
        y.append(eol())

        for one_clk in self.clocks:
            if one_clk != "__async__":
                y.append("process(" + one_clk + ")")
                y.append("begin")
                y.append(tab() + "if rising_edge(" + one_clk + ") then")
                y.append(tab(2) + "if " + self.global_rst + " = '1' then")
                for one_signal in self.signals:
                    if one_clk == self.clocks_by_name[one_signal.name]:
                        y.append(tab(3) + one_signal.name + " <= (others => '0');")
                y.append(tab(2) + "else")
                for one_signal in self.signals:
                    if one_clk == self.clocks_by_name[one_signal.name]:
                        y.append(tab(3) + one_signal.name + " <= " + self.expressions_by_name[one_signal.name] + ";")
                y.append(tab(2) + "end if;")
                y.append(tab() + "end if;")
                y.append("end process;")
                y.append(eol())
        for one_signal in self.outputs:
            y.append(one_signal.name + " <= " + self.expressions_by_name[one_signal.name] + ";")
        y.append(eol())
        y.append("end " + self.module_name + "_arch;")
        return y

    def render_module_verilog(self):
        raise NotImplemented()

    def render(self):
        raise NotImplemented


def test_entity():
    uut1 = Entity("my_fancy_box", default_clk="clk_100")
    # uut1.favor_fast_sim = True
    uut1.add_generic("width", datatype="integer")
    uut1.add_generic("rst_val")
    uut1.add_clk("clk_200")
    uut1.add_input("my_in_1")
    uut1.add_input("my_in_2")
    uut1.add_input("my_in_3")
    uut1.add_output("my_out_1")
    uut1.add_output("my_out_2")
    uut1.add_output("my_out_3")

    uut2 = Entity("my_fancy_submodule", default_clk="clk_200")
    uut2.add_generic("width", datatype="integer")
    uut2.add_generic("depth", datatype="integer")
    uut2.add_input("sub_mod_input_001")
    uut2.add_input("sub_mod_input_002")
    uut2.add_input("sub_mod_input_003")
    uut2.add_output("sub_mod_output_001")
    uut2.add_output("sub_mod_output_002")
    uut2.add_output("sub_mod_output_003")

    uut1.add_module(uut2)
    for one_line in uut1.render_module_vhdl():
        print(one_line)


if __name__ == "__main__":
    test_entity()





