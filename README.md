# cronpulse-lib

Minimal Python client library for interacting with the (placeholder) CronPulse monitoring API.

## Installation

```bash
pip install cronpulse-lib
```

## Quick Start

```python
from datetime import datetime, UTC, timedelta
from cronpulse_lib import CronPulse

client = CronPulse(api_key="YOUR_API_KEY")

# Create a monitor that expires in 1 day
monitor = client.create_monitor(
	name="Nightly Data Sync",
	interval=60,
	email="alerts@example.com",
	expires_at=datetime.now(UTC) + timedelta(days=1),
)

# Ping when your job runs
monitor.ping()

# Optionally delete
# monitor.delete()
```

## Versioning & Publishing

Releases are automated via GitHub Actions (trusted PyPI publishing) when pushing a tag matching `python-v*`.

## Development

Editable install with dev tools:

```bash
pip install -e python[dev]
pytest -q
```

## License

MIT
