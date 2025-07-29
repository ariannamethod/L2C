import os
import pytest
from health_check import check, shannon_entropy


def test_entropy():
    assert shannon_entropy('aaaa') == 0.0
    val = shannon_entropy('abcd')
    assert round(val, 2) == 2.0


@pytest.mark.skipif(not os.path.exists('weights/7B/model.bin'), reason='weights missing')
def test_check():
    metrics = check()
    assert 'available' in metrics
    assert 'entropy' in metrics

