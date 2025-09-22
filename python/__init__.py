import warnings
from cronpulse_lib import CronPulse, Monitor, __version__ as _lib_version

warnings.warn(
    "Root-level python package layout deprecated; use `import cronpulse_lib` instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["CronPulse", "Monitor", "__version__"]
__version__ = _lib_version
