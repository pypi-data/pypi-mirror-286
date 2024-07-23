"""
This is effectively an interface to pint. These are scattered throughout
different codebases, and it might make sense to consolidate them here.
"""

try:
    from functools import cache
except ImportError:
    from ubelt import memoize as cache


@cache
def unit_registry():
    """
    A memoized unit registry

    Returns:
        pint.UnitRegistry
    """
    import pint
    ureg = pint.UnitRegistry()
    return ureg
