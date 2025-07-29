import os
import pytest
from dream import dream, OUT_DIR


@pytest.mark.skipif(not os.path.exists('weights/7B/model.bin'), reason='weights missing')
def test_dream_file_creation():
    path = dream()
    assert os.path.exists(path)
    assert path.startswith(OUT_DIR)
    os.remove(path)


