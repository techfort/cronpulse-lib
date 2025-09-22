import warnings
from cronpulse_lib import CronPulse, Monitor  # forward import

warnings.warn(
    "`python/client.py` is deprecated; import from cronpulse_lib instead (e.g., from cronpulse_lib import CronPulse)",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["CronPulse", "Monitor"]
