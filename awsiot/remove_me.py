# TEMPORARY WIP FILE TO USE IN PLACE OF NON-ACCESSIBLE common.py from awscrt until a version is cut.
# DELETE THIS FILE and point to the correct location after crt has released a version with soft deprecation

"""
Cross-platform library for `awscrt`.
"""
from typing import TYPE_CHECKING
import _awscrt

__all__ = [
    "get_cpu_group_count",
    "get_cpu_count_for_group",
    "join_all_native_threads",
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


def get_cpu_group_count() -> int:
    """
    Returns number of processor groups on the system.

    Useful for working with non-uniform memory access (NUMA) nodes.
    """
    return _awscrt.get_cpu_group_count()


def get_cpu_count_for_group(group_idx: int) -> int:
    """
    Returns number of processors in a given group.
    """
    return _awscrt.get_cpu_count_for_group(group_idx)


def join_all_native_threads(*, timeout_sec: float = -1.0) -> bool:
    """
    Waits for all native threads to complete their join call.

    This can only be safely called from the main thread.
    This call may be required for native memory usage to reach zero.

    Args:
        timeout_sec (float): Number of seconds to wait before a timeout exception is raised.
            By default the wait is unbounded.

    Returns:
        bool: Returns whether threads could be joined before the timeout.
    """
    return _awscrt.thread_join_all_managed(timeout_sec)
