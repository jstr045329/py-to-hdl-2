"""Defines the interface to which all vendor packs will conform. We need volunteers
who have hardware from different vendors to flesh this out."""


class ClockManager:
    def __init__(self):
        raise notimplemented()
        pass

    def declare(self):
        raise notimplemented()

    def render(self):
        raise NotImplemented()


class ClockBuffer:
    def __init__(self):
        raise notimplemented()

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class InputBuffer:
    def __init__(self):
        raise notimplemented()

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class OutputBuffer:
    def __init__(self):
        raise notimplemented()

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()


class RamController:
    def __init__(self):
        raise notimplemented()

    def declare(self, differential=False):
        raise NotImplemented()

    def render(self, differential=False):
        raise NotImplemented()












