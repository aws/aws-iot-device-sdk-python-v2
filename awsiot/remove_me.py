# TEMPORARY WIP FILE TO USE IN PLACE OF NON-ACCESSIBLE common.py from awscrt until a version is cut.
# DELETE THIS FILE and point to the correct location after crt has released a version with soft deprecation

"""
Cross-platform library for `awscrt`.
"""
from typing import TYPE_CHECKING

__all__ = [
    "deprecated",
]

# At type-check time, expose a real symbol so linters/IDEs understand it.
# At runtime, prefer typing_extensions; fall back to typing (Py3.13+); else no-op.
if TYPE_CHECKING:
    # Static analysers will always attempt to import deprecated from typing_extensions and
    # fall back to known interpretation of `deprecated` if it fails and appropriately handle
    # the `@deprecated` tags.
    from typing_extensions import deprecated as deprecated
else:
    _deprecated_impl = None
    try:
        # preferred import of deprecated
        from typing_extensions import deprecated as _deprecated_impl
    except Exception:
        try:
            from typing import deprecated as _deprecated_impl  # Python 3.13+
        except Exception:
            _deprecated_impl = None

    def deprecated(msg=None, *, since=None):
        if _deprecated_impl is None:
            def _noop(obj): return obj
            return _noop
        if since is not None:
            try:
                return _deprecated_impl(msg, since=since)
            except TypeError:
                # older typing_extensions doesn't support the 'since' kwarg
                pass
        return _deprecated_impl(msg)
