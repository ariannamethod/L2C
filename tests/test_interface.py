import os
import json
import threading
import time
import http.client
import pytest

import interface


@pytest.mark.skipif(not os.path.exists('weights/7B/model.bin'), reason='weights missing')
def test_chat_endpoint():
    server = interface.create_server()
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        time.sleep(0.5)
        conn = http.client.HTTPConnection('localhost', 8000)
        payload = json.dumps({'prompt': 'Hello'})
        conn.request('POST', '/chat', body=payload, headers={'Content-Type': 'application/json'})
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        assert resp.status == 200
        result = json.loads(data)
        assert 'response' in result
    finally:
        server.shutdown()
        thread.join()
