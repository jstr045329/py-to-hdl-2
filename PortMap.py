"""Contains a class that stores port maps"""
from Signal import Signal


class PortMap:
    def __init__(self, module_name):
        self.module_ports = []
        self.map_to = []
        self.module_name = module_name
        self.inputs = set()
        self.inputs_assigned = set()
        self.outputs = set()
        self.outputs_assigned = set()
        self.generics = set()
        self.generics_assigned = set()

    def add_edge(self, one_module_port, one_dest_port="__route_out__"):
        assert(one_module_port not in self.module_ports)
        assert(one_dest_port not in self.map_to)
        assert(isinstance(one_module_port, Signal))
        assert(isinstance(one_dest_port, Signal) or
               one_dest_port == "__route_out__" or
               one_dest_port == "__open__")
        self.module_ports.append(one_module_port)
        self.map_to.append(one_dest_port)

    def declare_vhdl(self):
        # todo: finish this
        raise NotImplemented()

    def declare_verilog(self):
        # todo: finish this
        raise NotImplemented()

    def use_vhdl(self):
        # todo: finish this
        raise NotImplemented()

    def use_verilog(self):
        # todo: finish this
        raise NotImplemented()

