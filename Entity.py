from copy import deepcopy
from EngineeringUnits import Inf
from Signal import Signal
from ValidateMode import validate_mode


def validate_default_datatype(s):
    assert(s == "bit" or s == "std_logic" or s == "std_ulogic")


DEFAULT_GLOBAL_RESET_NAME = "rst_global"


class Entity:
    def __init__(self, **kwargs):
        """If you include the default_bit_value keyword argument, you must
        wrap the value in any necessary quotes."""
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
        self.inputs = set()
        self.outputs = set()
        self.declared_inputs = set()
        self.declared_outputs = set()
        self.signals = set()
        self.generics = set()
        self.components = set()
        self.child_modules = set()
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
        self.map_component_ports_to_similar_inputs = True
        self.map_component_ports_to_similar_outputs = True
        self.map_internal_signals_to_similar_port_names = True  # todo: decide whether this is really a good idea
        self.error_on_multiple_driver_candidates_for_output = True
        self.favor_fast_sim = True
        self.fast_datatype = "bit"
        self.accurate_datatype = "std_logic"

    def find_routable_signals(self):
        for one_sig in self.signals:
            if one_sig.should_route_source():
                new_sig = deepcopy(one_sig)
                new_sig.layers_to_route_source -= 1
                new_sig.name = ""  # todo: finish this
                self.inputs.add(new_sig)
            if one_sig.should_route_sink():
                new_sig = deepcopy(one_sig)
                new_sig.layers_to_route_source -= 1
                new_sig.name = ""  # todo: finish this
                self.outputs.add(new_sig)
        for one_port_map in self.port_maps:
            for a, b in zip(one_port_map.module_ports, one_port_map.map_to):
                if b == "__route_out__":
                    new_sig = deepcopy(a)
                    if new_sig.should_route_source:
                        if new_sig.layers_to_route_source < Inf:
                            new_sig.layers_to_route_source -= 1
                    if new_sig.should_route_sink:
                        if new_sig.layers_to_route_sink:
                            new_sig.layers_to_route_sink -= 1
                else:
                    # todo: finish this
                    raise NotImplemented()

    def set_as_top_level(self):
        self.double_buffer_inputs = True
        self.instantiate_rst_module = True
        self.route_clks_through_high_fanout = True

    def add_parent(self, p):
        assert(self.parent is None)  # Enforce calling this function once
        self.parent = p
        if self.inherit_parent_datatypes:
            self.accurate_datatype = p.accurate_datatype
            self.fast_datatype = p.fast_datatype
            self.favor_fast_sim = p.favor_fast_sim
        self.parent.child_modules.add(self)

    def instantiate_child(self, **kwargs):
        """Pass in the port map through kwargs"""
        # todo: finish this
        pass

    def set_as_unclocked(self):
        self.disable_clk_rendering = True
        self.is_synchronous = False

    def render_declaration_vhdl(self):
        raise NotImplemented()

    def render_declaration_verilog(self):
        raise NotImplemented()

    def render_port_map_vhdl(self):
        raise NotImplemented()

    def render_port_map_verilog(self):
        raise NotImplemented()

    def render_module_vhdl(self):
        """Includes entity declaration"""
        raise NotImplemented()

    def render_module_verilog(self):
        raise NotImplemented()

    def render(self):
        raise NotImplemented

# todo: Come up with a good way to handle automatic signal routing.from
#       Could be as simple as
