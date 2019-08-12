"""Defines the interface to which all vendor packs will conform."""


class ClockManager:
    def __init__(self):
        pass

    def declare(self):
        raise NotImplemented()

    def render(self):
        raise NotImplemented()


class ClockBuffer:
    def __init__(self):
        pass

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class InputBuffer:
    def __init__(self):
        pass

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class OutputBuffer:
    def __init__(self):
        pass

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class RamController:
    def __init__(self):
        pass

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()












