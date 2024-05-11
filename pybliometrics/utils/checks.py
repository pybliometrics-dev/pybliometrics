def check_parameter_value(parameter, allowed, name):
    """Raise a ValueError if a parameter value is not in the set of
    allowed values.
    """
    if parameter not in allowed:
        raise ValueError(f"Parameter '{name}' must be one of {', '.join(allowed)}.")
