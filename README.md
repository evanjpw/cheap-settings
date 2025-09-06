# Cheap Settings

_A lightweight, low footprint settings system_

`cheap-settings` is a Python package for providing a very simple, very low impact, configuration. The Python
configuration & settings landscape is virtually overflowing with clever, advanced, flexible solutions that cover
many needs. However, what _I_ needed was a bit different from any config/settings package that I was aware of.

The main thing that distinguishes `cheap_settings` from any alternative solutions is simplicity: it is _extremely_
simple (& ergonomic) to use, & it intentionally limits its scope & feature set to be simple to understand.

Additionally, it supports circumstances where it is difficult to bring your config file with you. All of your config
is defined in the code or in the environment.

## OK, How Does it Actually Work?

Define your settings class as a subclass of `CheapSettings`. Add your settings values to your class as class attributes.
Add type hints so `cheap_settings` knows how to convert values. Add initializers for your def values of the settings.

At runtime, `cheap_settings` will read any environment variable with the same name as your attributes, *and override
the attribute value, automatically converting to the correct type (even for Optional types)*.

Then, from anywhere in your code, you can use `MySettings.MY_VALUE`.

It intentionally doesn't allow you to access environment variables that don't have a corresponding attribute assigned in
your settings class, because you want to know if you are not using the correct setting name.

That's it. That's what it does (& nothing else).

```python
from os import environ
from typing import Optional
from cheap_settings import CheapSettings

class MySettings(CheapSettings):
    MAX_ANNOYANCE: int = 0
    ANNOYANCE_FACTOR: float = 0.0
    ANNOYANCE_NAME: str = ""
    ANNOYANCE_ATTRIBUTES: list = []
    AM_I_ANNOYED: bool = False
    HOW_ANNOYED_EACH_DAY: dict = {}
    # Python 3.10+ union syntax also works: `OPTIONAL_ANNOYANCE: float | None = None`
    OPTIONAL_ANNOYANCE: Optional[float] = None

# As you would expect:
assert MySettings.MAX_ANNOYANCE == 0
assert MySettings.ANNOYANCE_FACTOR == 0.0
assert MySettings.ANNOYANCE_NAME == ""
assert MySettings.ANNOYANCE_ATTRIBUTES == []
assert MySettings.AM_I_ANNOYED is False
assert MySettings.HOW_ANNOYED_EACH_DAY ==  {}
assert MySettings.OPTIONAL_ANNOYANCE is None

# But what if we now set some environment variables?

environ["MAX_ANNOYANCE"] = "100"
environ["ANNOYANCE_FACTOR"] = "2.71828"
environ["ANNOYANCE_NAME"] = "leaf blowers"
environ["ANNOYANCE_ATTRIBUTES"] = '["noise!", "exhaust"]'  # Any valid JSON array
environ["AM_I_ANNOYED"] = "true"  # "true"/"false", "1"/"0", "yes"/"no", "on"/"off" (case-insensitive)
environ["HOW_ANNOYED_EACH_DAY"] = '{"Monday": "10%", "Tuesday": "90%"}'  # Any valid JSON object
environ["OPTIONAL_ANNOYANCE"] = "32.767"  # or "none" to set to None for Optional types

# Now

assert MySettings.MAX_ANNOYANCE == 100  # It's known to be an int from the type hint
assert MySettings.ANNOYANCE_FACTOR == 2.71828  # Float works the same way
assert MySettings.ANNOYANCE_NAME == "leaf blowers"
assert MySettings.ANNOYANCE_ATTRIBUTES == ["noise!", "exhaust"]  # Converts to list
assert MySettings.AM_I_ANNOYED is True  # Case-insensitive conversion of "true" or "false"
assert MySettings.HOW_ANNOYED_EACH_DAY ==  {"Monday": "10%", "Tuesday": "90%"}  # Converts to a dict
assert MySettings.OPTIONAL_ANNOYANCE == 32.767  # Correctly converts with Optional types (or type unions!)
```

You can also use inheritance:

```python
from cheap_settings import CheapSettings

class BaseSettings(CheapSettings):
    host: str = "localhost"
    port: int = 8080

class TestSettings(BaseSettings):
    debug: bool = True  # Inherits host and port from BaseSettings
```

## Installation

Really? Really? You're looking for a settings/config manager for your Python code, & you want me to tell you how to
use `pip`. OK, cool. I'm happy to help, really:

```shell
pip install cheap-settings
```

## TBD - Features to be Added

* Settings without initializers
* Use the initializer type as the setting type (no type hint needed)
* Selectable different configurations for different environments (for example, DEV, STAGING, PROD)
* Expanded type support: `datetime`, `date`, `time`, `pathlib.Path`, `Decimal`, `UUID`, custom types with
 `from_string()` methods
* Custom validators & converters for field-level validation and custom conversion functions

## Alternatives

You probably don't actually want to use this. There are probably superior alternatives for what you are trying to do.
For example:

* [betterconf](https://github.com/prostomarkeloff/betterconf) - This is remarkably similar to `cheap_settings`, but,
 better (it's right in the name). It has more features & does more stuff, at the cost of some complexity.
* [conftier](https://github.com/Undertone0809/conftier) - Also similar in some ways, & also very cool. Also, quite a
 bit more complexity.
* [python-config2](https://github.com/grimen/python-config2) - Also kind of similar. More features, more complexity.
* Python's own, built-in [configparser](https://docs.python.org/3/library/configparser.html) - This does things a
 different way, but it's built into Python, so you do not need any dependencies.
* Roll your own - The simplest is to be old school & write a `settings.py` & be done with it.

# Contributing

If you _do_ decide to use this, I welcome your suggestions, comments, or pull requests.

> Imagine a clever, relevant quote here.

# License

This project is licensed under MIT License.

See [LICENSE](./LICENSE) for details.
