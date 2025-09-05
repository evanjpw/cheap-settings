import json
import os

# TODO: Deal with Optional types & type unions (& algebraic types) by using `issubclass`
def _convert_value_to_type(value, to_type):
    """"""
    if value is not None and isinstance(value, str):
        if to_type == int:
            return int(value)
        elif to_type == float:
            return float(value)
        elif to_type == bool:
            normalized_value = value.lower()
            if normalized_value == 'true':
                return True
            elif normalized_value == 'false':
                return False
            else:
                raise ValueError(f"{value} is not a valid boolean value")
        elif to_type in [list, dict]:
            parsed_value = json.loads(value)
            if to_type == list and not isinstance(parsed_value, list):
                raise ValueError(f"{value} is not a list")
            if to_type == dict and not isinstance(parsed_value, dict):
                raise ValueError(f"{value} is not a dict")
            return parsed_value

    return value

# TODO: Implement __delattr__ & __dir__
class MetaCheapSettings(type):
    """"""

    class ConfigInstance:
        pass
    # TODO: See https://docs.python.org/3/howto/annotations.html#annotations-howto
    def __new__(mcs, name, bases, dct):
        config_instance = mcs.ConfigInstance()
        annotations = dct.pop('__annotations__', {})
        config_instance.__annotations__ = annotations
        for key, value in dct.items():
            setattr(config_instance, key, value)
            del dct[key]
        dct['__config_instance'] = config_instance
        return super().__new__(mcs, name, bases, dct)

    def __getattribute__(cls, attribute):
        config_instance = cls.__config_instance
        if hasattr(config_instance, attribute):
            env_attr = os.environ.get(attribute.upper())
            if env_attr is not None:
                return _convert_value_to_type(env_attr, config_instance.__annotations__[attribute])
            return getattr(config_instance, attribute)
        raise AttributeError(attribute)

    def __setattr__(cls, attribute, value):
        config_instance = cls.__config_instance
        setattr(config_instance, attribute, value)


class CheapSettings(metaclass=MetaCheapSettings):
    """"""
