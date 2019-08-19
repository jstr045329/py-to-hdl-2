"""Contains a class for storing port maps."""
from WhiteSpaceTools import eol, tab


class PortMap:
    def __init__(self, module_name, instance_label=None):
        self.module_ports = []
        self.map_to = []
        self.module_name = module_name
        self.instance_label = instance_label

    def add_edge(self, one_module_port, one_dest_port="__route_out__"):
        assert(one_module_port not in self.module_ports)
        assert(one_dest_port not in self.map_to)
        self.module_ports.append(one_module_port)
        self.map_to.append(one_dest_port)

    def declare_vhdl(self):
        return []

    def declare_verilog(self):
        return []

    def render_vhdl(self):
        y = []
        one_str = ""
        if self.instance_label is not None:
            one_str += self.instance_label + ": "
        one_str += self.module_name
        y.append(one_str)
        y.append("port map(")
        for i in range(len(self.module_ports)):
            one_str = tab() + self.module_ports[i] + " => " + self.map_to[i]
            one_str += "," if i < len(self.module_ports) - 1 else ");"
            y.append(one_str)
        return y

    def render_verilog(self):
        # todo: finish this
        raise NotImplemented()

