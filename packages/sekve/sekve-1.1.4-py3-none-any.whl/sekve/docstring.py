def copy(source):
    """Copy a docstring from another source function (if present)."""
    def do_copy(target):
        if source.__doc__:
            target.__doc__ = source.__doc__
        return target
    return do_copy


def add(docstring):
    """Copy a docstring from another source function (if present)."""
    def do_add(target):
        if docstring:
            target.__doc__ += docstring
        return target
    return do_add
