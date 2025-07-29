import ctypes
import os
import logging

logger = logging.getLogger(__name__)

_lib = None


def _load_lib():
    global _lib
    if _lib:
        return _lib
    lib_path = os.path.join(os.path.dirname(__file__), 'libl2c.so')
    if not os.path.exists(lib_path):
        raise FileNotFoundError('libl2c.so not found. Run `make lib` first.')
    _lib = ctypes.CDLL(lib_path)
    _lib.l2c_generate.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                                 ctypes.c_int, ctypes.c_float, ctypes.c_float]
    _lib.l2c_generate.restype = ctypes.c_void_p
    _lib.l2c_free.argtypes = [ctypes.c_void_p]
    _lib.l2c_free.restype = None
    return _lib


def generate(prompt: str, checkpoint: str = 'weights/7B/model.bin', steps: int = 256,
             temperature: float = 1.0, topp: float = 0.9) -> str:
    """Generate text from prompt using the L2C core."""
    lib = _load_lib()
    if prompt is None:
        prompt = ''
    result_ptr = None
    try:
        result_ptr = lib.l2c_generate(checkpoint.encode('utf-8'),
                                      prompt.encode('utf-8'),
                                      steps, temperature, topp)
        if not result_ptr:
            raise RuntimeError('C generation returned NULL')
        output = ctypes.string_at(result_ptr).decode('utf-8')
        return output
    finally:
        if result_ptr:
            lib.l2c_free(result_ptr)


def dream_once() -> str:
    """Generate a single dream and return the path to the saved file."""
    from dream import dream

    return dream()


def dream_loop(delay: int = 5) -> None:
    """Continuously generate dreams every ``delay`` seconds."""
    import time

    while True:
        path = dream_once()
        print('dream saved to', path)
        time.sleep(delay)


def health() -> dict:
    """Return health metrics from :mod:`health_check`."""
    from health_check import check

    return check()


def tokenize_file(path: str):
    """Tokenize contents of ``path`` using :mod:`tokenizer`."""
    from tokenizer import Tokenizer

    tok = Tokenizer()
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return tok.encode(text, bos=True, eos=False)


def train(dataset_path: str) -> None:
    """Placeholder training routine."""
    logger.info('Training on %s (stub implementation)', dataset_path)



