import os
import pytest
from l2c import generate


@pytest.mark.skipif(not os.path.exists('weights/7B/model.bin'), reason='weights missing')
def test_generate_text():
    out = generate('hello', steps=8)
    assert isinstance(out, str)
    assert len(out) > 0


@pytest.mark.skipif(not os.path.exists('weights/7B/model.bin'), reason='weights missing')
def test_generate_empty():
    out = generate('', steps=8)
    assert isinstance(out, str)

