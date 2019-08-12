from EngineeringUnits import Inf


class Signal:
    """Use this for clocks, resets, and logic signals"""
    def __init__(self,
                 nm,
                 speed=None,
                 fanout=False,
                 layers_to_route_source=0,
                 layers_to_route_sink=0,
                 clk_to_sync_with=None,
                 expr="",
                 default_val=None,
                 width=1):
        self.name = nm
        self.speed = speed
        self.width = width
        self.fanout = fanout
        self.layers_to_route_source = layers_to_route_source
        self.layers_to_route_sink = layers_to_route_sink
        self.parent = None
        self.drive_with_differential_buf = False
        self.sink_to_differential_buf = False
        self.drive_with_top_level_buf = False
        self.sink_to_top_level_buf = False
        self.enforce_single_driver = True
        self.sources = set()
        self.sinks = set()
        self.clk_to_sync_with = clk_to_sync_with
        self.expression = expr
        self.default_val = default_val
        self.use_default_val = False if default_val is None else True
        self.is_clock = False
        self.is_input = False
        self.is_output = False
        self.is_generic = False
        self.is_signal = True
        self.number_of_receivers = 0

        if self.drive_with_top_level_buf:
            self.layers_to_route_source = Inf
        if self.sink_to_top_level_buf:
            self.layers_to_route_sink = Inf

    def make_it_a_clock(self):
        self.is_clock = True
        self.is_input = False
        self.is_output = False
        self.is_generic = False
        self.is_signal = False

    def make_it_an_input(self):
        self.is_clock = False
        self.is_input = True
        self.is_output = False
        self.is_generic = False
        self.is_signal = False

    def make_it_an_output(self):
        self.is_clock = False
        self.is_input = False
        self.is_output = True
        self.is_generic = False
        self.is_signal = False

    def make_it_a_generic(self):
        self.is_clock = False
        self.is_input = False
        self.is_output = False
        self.is_generic = True
        self.is_signal = False

    def make_it_a_signal(self):
        self.is_clock = False
        self.is_input = False
        self.is_output = False
        self.is_generic = False
        self.is_signal = True

    def should_route_source(self):
        if self.layers_to_route_source == Inf:
            return True
        return self.layers_to_route_source > 0

    def should_route_sink(self):
        if self.layers_to_route_sink == Inf:
            return True
        return self.layers_to_route_sink > 0

    def add_source(self, one_source):
        self.sources.append(one_source)

    def add_sink(self, one_sink):
        self.sinks.append(one_sink)

    def declare(self):
        # todo: finish this
        raise NotImplemented()

    def use(self):
        if self.enforce_single_driver:
            assert(len(self.sources) == 1)
        # todo: finish this
        raise NotImplemented()

    def __hash__(self):
        # todo: finish this
        pass

    def __eq__(self, other):
        # todo: finish this
        pass


