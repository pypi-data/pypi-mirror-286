import beartype

__all__ = ["typecheck"]

# Do not raise exceptions and stop the execution of the code, when a type
# violation is found. Instead, print a warning message.
_conf = beartype.BeartypeConf(violation_type=UserWarning)

# Create a typecheck decorator that will be used to typecheck the functions.
typecheck = beartype.beartype(conf=_conf)
