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
    def load_module(cls, module_name, select=lambda subclass: True):
        """
        Return the class given by module_name

        :param      cls:          Pointer to this class
        :type       cls:          Plugin
        :param      module_name:  The name of the module
        :type       module_name:  None or str
        :param      select:       A function given to filter() to filter the
                                  subclasses list
        :type       select:       Function

        :returns:   The class.
        :rtype:     Plugin

        :raises     Exception:    If the class does not exist in module
        """
        module_name = cls.get_value(module_name, cls._module_name)
        import_module(module_name, package='all_seeing_eye')
        subclasses = cls.__subclasses__()
        subclasses = list(filter(select, subclasses))
        if len(subclasses) > 1:
            raise Exception(f'More than one {cls._type} module: {subclasses}')
        if not subclasses or module_name not in str(subclasses[0]):
            raise Exception(f'{cls._type} module {module_name} does not exist '
                            f'or does not subclass {cls.__class__.__name__}')
        return subclasses[0]

    @classmethod
    def get_value(cls, *args):
        """
        Return the first value that is not None

        :param      args:       The argument list
        :type       args:       list

        :returns:   The value.
        :rtype:     Any, but not None

        :raises     Exception:  If all arguments are None
        """
        for arg in filter(lambda x: x is not None, args):
            return arg
        raise Exception("All arguments are None")

    @classmethod
    def get_class(cls, module_name=None):
        m = cls.get_value(module_name, cls._module_name)
        return cls.load_module(m, lambda subclass: m in str(subclass))

    @classmethod
    def get_instance(cls, module_name=None, *args, **kwargs):
        if not cls._instance:
            subclass = cls.load_module(module_name)
            cls._instance = subclass(*args, **kwargs)
        return cls._instance
