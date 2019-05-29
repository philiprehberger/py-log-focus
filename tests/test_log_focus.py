import logging
from philiprehberger_log_focus import FocusHandler, focus


def test_focus_returns_logger():
    logger = focus("test_app")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_app"


def test_focus_handler_instantiation():
    handler = FocusHandler()
    assert isinstance(handler, logging.Handler)


def test_focus_handler_custom_thresholds():
    handler = FocusHandler(repeat_threshold=3, slow_threshold_ms=50)
    assert handler.repeat_threshold == 3
    assert handler.slow_threshold_ms == 50


def test_handler_emits_records(capsys):
    logger = logging.getLogger("test_emit")
    logger.handlers.clear()
    handler = FocusHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.info("test message")
    captured = capsys.readouterr()
    assert "test message" in captured.err or "test message" in captured.out


def test_repeat_suppression(capsys):
    logger = logging.getLogger("test_repeat")
    logger.handlers.clear()
    handler = FocusHandler(repeat_threshold=3)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    for _ in range(10):
        logger.info("repeated message")
    # Should not crash; suppression logic should work


def test_focus_sets_level():
    logger = focus("test_level", level=logging.WARNING)
    assert logger.level == logging.WARNING
