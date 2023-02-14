from abc import ABC, abstractmethod
from importlib import import_module
from dataclasses import dataclass
from typing import List, Generator, Dict

@dataclass
class Plugin(ABC):
    """
    Interface for a PDF library
    """
    _instance = None
    _class = None
    _module_name = None
    _type = 'plugin'

    @classmethod
    def get_instance(cls, module_name = None, *args, **kwargs):
        if not cls._instance:
            module_name = module_name if module_name is not None else cls._module_name
            import_module(module_name)
            subclasses = cls.__subclasses__()
            if len(subclasses) > 1:
                raise Exception(f'More than one {cls._type} module: {subclasses}')
            if not subclasses or module_name not in str(subclasses[0]):
                raise Exception(f'{cls._type} module {module_name} does not exist or does not subclass {__class__.__name__}')
            cls._instance = subclasses[0](*args, **kwargs)
        return cls._instance

    @classmethod
    def get_class(cls, module_name = None, *args, **kwargs):
        if not cls._class:
            module_name = module_name if module_name is not None else cls._module_name
            import_module(module_name)
            subclasses = cls.__subclasses__()
            if len(subclasses) > 1:
                raise Exception(f'More than one {cls._type} module: {subclasses}')
            if not subclasses or module_name not in str(subclasses[0]):
                raise Exception(f'{cls._type} module {module_name} does not exist or does not subclass {__class__.__name__}')
            cls._class = subclasses[0]
        return cls._class
