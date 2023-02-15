from abc import ABC
from importlib import import_module
from dataclasses import dataclass, field
from typing import Optional, Type


@dataclass
class Plugin(ABC):
    """
    Interface for a PDF library
    """
    _module_name: Optional[str] = field(default=None)
    _instance: Optional[Type['Plugin']] = field(default=None, init=False)
    _class: Optional[Type['Plugin']] = field(default=None, init=False)
    _type: str = field(default='plugin', init=False)

    @classmethod
    def load_module(cls, module_name):
        module_name = module_name if module_name is not None else cls._module_name
        import_module(module_name, package='all_seeing_eye')
        subclasses = cls.__subclasses__()
        if len(subclasses) > 1:
            raise Exception(f'More than one {cls._type} module: {subclasses}')
        if not subclasses or module_name not in str(subclasses[0]):
            raise Exception(f'{cls._type} module {module_name} does not exist '
                            f'or does not subclass {cls.__class__.__name__}')
        return subclasses[0]

    @classmethod
    def get_class(cls, module_name=None):
        if not cls._class:
            cls._class = cls.load_module(module_name)
        return cls._class

    @classmethod
    def get_instance(cls, module_name=None, *args, **kwargs):
        if not cls._instance:
            subclass = cls.get_class(module_name)
            cls._instance = subclass(*args, **kwargs)
        return cls._instance
