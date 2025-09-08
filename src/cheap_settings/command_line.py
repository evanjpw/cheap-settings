import argparse
from typing import Optional


def _convert_to_argument_name(name: str) -> str:
    """Convert an attribute name to an argument name."""
    name = name.lower()
    return name.replace("_", "-")


def _bool_str_to_bool(value: str) -> bool:
    normalized_value = value.lower()
    if normalized_value in ("true", "1", "yes", "on"):
        return True
    elif normalized_value in ("false", "0", "no", "off"):
        return False
    else:
        raise ValueError(f"{value} is not a valid boolean value")


def _get_arg_parser(
    config_instance, parser: Optional[argparse.ArgumentParser] = None
) -> argparse.ArgumentParser:
    """Create an argument parser from the given config instance. Creates an argument
    parser, or uses the supplied parser if present, then iterates through
    the config instance's attributes, converting them to argument names, & adds
    them as arguments to the parser, using the attribute's type annotations
    to determine the argument type. Returns an argument parser instance."""
    if parser is None:
        parser = argparse.ArgumentParser()

    # Get annotations directly from the config instance
    annotations = getattr(config_instance, "__annotations__", {})

    # Reserved argument names that conflict with argparse built-ins
    reserved_args = {"help", "h"}

    # Process both attributes and annotations
    all_names = set(dir(config_instance)) | set(annotations.keys())

    for name in all_names:
        if name.startswith("_"):
            continue

        # Check for reserved names
        if name.lower() in reserved_args:
            raise ValueError(
                f"Cannot use '{name}' as a setting name because it conflicts with argparse built-in options. "
                f"Reserved names: {', '.join(sorted(reserved_args))}"
            )

        argument_name = _convert_to_argument_name(name)
        argument_type = annotations.get(name)
        argument_default = getattr(config_instance, name, None)
        argument_action = "store"

        if argument_type is None:
            argument_type = type(argument_default) or str

        # Handle Optional/Union types for argparse
        from typing import get_args, get_origin

        origin = get_origin(argument_type)
        if origin is not None:
            # For Optional/Union types, extract the non-None type
            args = get_args(argument_type)
            for arg in args:
                if arg is not type(None):
                    argument_type = arg
                    break

        if argument_type == bool:
            if argument_default is None:
                argument_type = _bool_str_to_bool
            elif argument_default is False:
                argument_action = "store_true"
            elif argument_default is True:
                # TODO: This should probably be improved to handle a variety of names
                argument_name = "no-" + argument_name
                argument_action = "store_false"
            else:
                ...
                # TODO: Should we `raise` here? Should we do something different from that? Same as `None`?
        elif argument_type in (dict, list):
            # TODO: Eventually, handle these. For now, we should document that we don't handle them & they are _NOT_
            #  added as command lNe arguments.
            continue

        argument_name = "--" + argument_name

        # store_true/store_false don't accept type parameter
        if argument_action in ("store_true", "store_false"):
            parser.add_argument(
                argument_name,
                default=argument_default,
                action=argument_action,
                dest=name,
            )
        else:
            parser.add_argument(
                argument_name,
                type=argument_type,
                default=argument_default,
                action=argument_action,
                dest=name,
            )

    return parser


def _incorporate_parsed_arguments(
    args: argparse.Namespace, config_instance, cli_config_instance, provided_args
):
    """Updates the cli_config_instance with only the arguments that were explicitly provided.
    As designed, command line args will always override environment variables."""
    # Get annotations directly from the config instance
    annotations = getattr(config_instance, "__annotations__", {})
    # Create the cli config annotations dict if not already present
    if not hasattr(cli_config_instance, "__annotations__"):
        cli_config_instance.__annotations__ = {}

    # Convert provided args to a string for checking
    args_str = " ".join(provided_args) if provided_args else ""

    for name, value in vars(args).items():
        if hasattr(config_instance, name) or name in annotations:
            # Check if this argument was actually provided on the command line
            arg_name = "--" + _convert_to_argument_name(name)
            no_arg_name = "--no-" + _convert_to_argument_name(name)

            # Only set if the argument was explicitly provided
            if arg_name in args_str or no_arg_name in args_str:
                setattr(cli_config_instance, name, value)
                # TODO: The Python documentation says that one should not do this, ever
                if name in annotations:
                    cli_config_instance.__annotations__[name] = annotations[name]


def parse_command_line_arguments(
    config_instance,
    cli_config_instance,
    parser: Optional[argparse.ArgumentParser] = None,
    args=None,
) -> argparse.Namespace:
    """Creates an argument parser from the config instance, then
    Parses the command line arguments and returns an argparse.Namespace.

    Args:
        config_instance: The config instance to read settings from
        cli_config_instance: The config instance to store CLI values
        parser: Optional custom ArgumentParser
        args: Optional list of arguments to parse (if None, uses sys.argv)
    """
    import sys

    parser = _get_arg_parser(config_instance, parser)
    parsed_args = parser.parse_args(args)
    # Pass the actual args that were provided
    provided_args = args if args is not None else sys.argv[1:]
    _incorporate_parsed_arguments(
        parsed_args, config_instance, cli_config_instance, provided_args
    )
    return parsed_args
