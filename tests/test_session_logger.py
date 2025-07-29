import importlib
import json
import os
import sys


def test_log_turn(tmp_path, monkeypatch):
    monkeypatch.setenv("L2C_LOG_DIR", str(tmp_path))
    if "session_logger" in sys.modules:
        del sys.modules["session_logger"]
    session_logger = importlib.import_module("session_logger")
    session_logger.log_turn("hi", "there")
    assert os.path.exists(session_logger.SESSION_FILE)
    with open(session_logger.SESSION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["session_id"] == session_logger.SESSION_ID
    assert data["turns"] == [{"user": "hi", "l2c": "there"}]
