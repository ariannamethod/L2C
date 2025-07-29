import http.client
import importlib
import json
import os
import sys
import threading
import time

import pytest


@pytest.mark.skipif(
    not os.path.exists("weights/7B/model.bin"), reason="weights missing"
)
def test_chat_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("L2C_LOG_DIR", str(tmp_path))
    if "session_logger" in sys.modules:
        del sys.modules["session_logger"]
    if "interface" in sys.modules:
        del sys.modules["interface"]
    interface = importlib.import_module("interface")
    server = interface.create_server()
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        time.sleep(0.5)
        conn = http.client.HTTPConnection("localhost", 8000)
        payload = json.dumps({"prompt": "Hello"})
        conn.request(
            "POST", "/chat", body=payload, headers={"Content-Type": "application/json"}
        )
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        assert resp.status == 200
        result = json.loads(data)
        assert "response" in result
        files = list(tmp_path.glob("*.json"))
        assert len(files) == 1
        with open(files[0], "r", encoding="utf-8") as f:
            logged = json.load(f)
        assert logged["turns"][0]["user"] == "Hello"
    finally:
        server.shutdown()
        thread.join()
