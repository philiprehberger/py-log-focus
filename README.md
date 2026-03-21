# philiprehberger-log-focus

[![Tests](https://github.com/philiprehberger/py-log-focus/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-log-focus/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-log-focus.svg)](https://pypi.org/project/philiprehberger-log-focus/)
[![License](https://img.shields.io/github/license/philiprehberger/py-log-focus)](LICENSE)

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

- Color-coded output by log level (DEBUG=gray, INFO=default, WARNING=yellow, ERROR=red, CRITICAL=bold red)
- Repeat suppression — collapses repeated identical messages
- Slow operation highlighting via `extra["duration_ms"]`

## API

| Function / Class | Description |
|------------------|-------------|
| `focus(name, level="WARNING")` | Quick setup, returns a configured logger |
| `FocusHandler(level, repeat_threshold, slow_key, slow_threshold_ms, stream)` | Custom logging handler with color and repeat suppression |
| `Colors` | ANSI escape constants — `RESET`, `BOLD`, `DIM`, `RED`, `YELLOW`, `GRAY` |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
