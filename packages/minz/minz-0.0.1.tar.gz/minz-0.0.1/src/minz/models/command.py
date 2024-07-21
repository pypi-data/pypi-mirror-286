from typing import List
from itertools import zip_longest

ANY = object()

class ArgParseError(Exception):
    pass

class BaseArgv:
    pass

ARGUMENT = 'ARGUMENT'
FLAG_SHORT = 'FLAG_SHORT'
FLAG_LONG = 'FLAG_LONG'

NO_DEFAULT = object()

class Argument(BaseArgv):
    """
    Argument class
    NOTE: _types are *weak*, only validators return errors. _types return None if the type cant be parsed
    """
    def __init__(self, name: str, kind, _type = ANY, validators = None, description: str = '', default = None):
        self.name = name
        self._type = _type
        self.validators = validators
        self.description = description
        self.default = default
        self.kind = kind


    def get_data(self):
        return {
            "name": self.name,
            "default": self.default,
            "description": self.description,
            "validators": self.validators or [],
        }

    def parse(self, arg):
        """
        validates and parses argument for passing to handler
        """
        if arg is None:
            if default is None:
                return ArgParseError("Required")
            return default

        if self._type is ANY:
            return arg
        if self._type in (int, str):
            try:
                return self._type(arg)
            except:
                return None
        raise NotImplementedError("error about bad config annotation")

class Command:

    def __init__(self, name, handler, flags: List = None, arguments: List[Argument] = None):
        self.name = name
        self.flags = flags or []
        self.arguments = arguments or []
        self.handler = handler

    
    def run(self, *uargs, **uflags):
        """
        run with supplied args/flags (u-prefixed)
        """
        prepared_args = zip_longest(self.args, args)
        



