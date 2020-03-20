"""Structured log filtering and highlighting for terminals."""

from __future__ import annotations

import logging
import sys
from typing import ClassVar


__all__ = [
    "FocusHandler",
    "Colors",
    "focus",
]


class Colors:
    """ANSI escape code constants for terminal coloring."""

    RESET: ClassVar[str] = "\033[0m"
    BOLD: ClassVar[str] = "\033[1m"
    DIM: ClassVar[str] = "\033[2m"
    RED: ClassVar[str] = "\033[31m"
    YELLOW: ClassVar[str] = "\033[33m"
    GRAY: ClassVar[str] = "\033[90m"


class FocusHandler(logging.Handler):
    """A logging handler that highlights important events in the terminal.

    Color-codes log messages by level, suppresses repeated messages,
    and highlights slow operations.

    Args:
        level: Minimum log level to display.
        repeat_threshold: After this many identical messages, suppress and show count.
        slow_key: Key in ``extra`` dict indicating operation duration in ms.
        slow_threshold_ms: Duration above which a log line is highlighted as slow.
        stream: Output stream. Defaults to ``sys.stderr``.
    """

    _LEVEL_STYLES: ClassVar[dict[int, str]] = {
        logging.DEBUG: Colors.DIM + Colors.GRAY,
        logging.INFO: "",
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED + Colors.BOLD,
    }

    def __init__(
        self,
        level: int = logging.DEBUG,
        repeat_threshold: int = 3,
        slow_key: str = "duration_ms",
        slow_threshold_ms: float = 1000,
        stream: object | None = None,
    ) -> None:
        super().__init__(level)
        self.repeat_threshold = repeat_threshold
        self.slow_key = slow_key
        self.slow_threshold_ms = slow_threshold_ms
        self.stream = stream or sys.stderr

        self._last_message: str = ""
        self._repeat_count: int = 0

    def emit(self, record: logging.LogRecord) -> None:
        """Format and emit a log record with color and repeat suppression."""
        try:
            msg = self.format(record) if self.formatter else record.getMessage()
            full_msg = f"[{record.levelname}] {msg}"

            if full_msg == self._last_message:
                self._repeat_count += 1
                if self._repeat_count >= self.repeat_threshold:
                    return
            else:
                self._flush_repeats()
                self._last_message = full_msg
                self._repeat_count = 1

            style = self._get_style(record)
            line = f"{style}{full_msg}{Colors.RESET}"

            self.stream.write(line + "\n")  # type: ignore[union-attr]
            self.stream.flush()  # type: ignore[union-attr]
        except Exception:
            self.handleError(record)

    def _get_style(self, record: logging.LogRecord) -> str:
        duration = getattr(record, self.slow_key, None)
        if duration is not None and float(duration) >= self.slow_threshold_ms:
            return Colors.BOLD + Colors.YELLOW

        for lvl in sorted(self._LEVEL_STYLES, reverse=True):
            if record.levelno >= lvl:
                return self._LEVEL_STYLES[lvl]
        return ""

    def _flush_repeats(self) -> None:
        if self._repeat_count > self.repeat_threshold:
            suppressed = self._repeat_count - self.repeat_threshold
            line = (
                f"{Colors.DIM}  ... repeated {suppressed} more "
                f"time{'s' if suppressed != 1 else ''}{Colors.RESET}"
            )
            self.stream.write(line + "\n")  # type: ignore[union-attr]
            self.stream.flush()  # type: ignore[union-attr]

    def close(self) -> None:
        """Flush any pending repeat counts before closing."""
        self._flush_repeats()
        super().close()


def focus(
    name: str | None = None,
    *,
    level: str | int = "WARNING",
) -> logging.Logger:
    """Configure a logger with a FocusHandler and return it.

    Convenience function for quick setup.

    Args:
        name: Logger name. ``None`` for the root logger.
        level: Minimum log level as string or int constant.

    Returns:
        The configured :class:`logging.Logger`.
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.WARNING)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(FocusHandler(level=level))
    return logger
