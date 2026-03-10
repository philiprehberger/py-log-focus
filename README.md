# philiprehberger-log-focus

Structured log filtering and highlighting for terminals.

## Installation

```bash
pip install philiprehberger-log-focus
```

## Usage

### Quick Setup

```python
from philiprehberger_log_focus import focus

logger = focus("myapp")
logger.info("Server started")
logger.warning("High memory usage")
logger.error("Connection failed")
```

### Custom Handler

```python
import logging
from philiprehberger_log_focus import FocusHandler

handler = FocusHandler(
    repeat_threshold=5,    # Suppress after 5 identical messages
    slow_threshold_ms=100, # Highlight slow operations
)

logger = logging.getLogger("myapp")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
```

### Slow Operation Highlighting

```python
logger.info("Query completed", extra={"duration_ms": 250})
# Automatically highlighted if above slow_threshold_ms
```

### Features

- Color-coded output by log level (DEBUG=cyan, INFO=green, WARNING=yellow, ERROR=red, CRITICAL=magenta)
- Repeat suppression — collapses repeated identical messages
- Slow operation highlighting via `extra["duration_ms"]`

## API

- `focus(name, level=DEBUG, repeat_threshold=10, slow_threshold_ms=100)` — Quick setup, returns a configured logger
- `FocusHandler(repeat_threshold, slow_threshold_ms)` — Custom logging handler

## License

MIT
