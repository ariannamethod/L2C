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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import argparse
    parser = argparse.ArgumentParser(description='Generate text with L2C')
    parser.add_argument('prompt', nargs='?', default='')
    parser.add_argument('--checkpoint', default='weights/7B/model.bin')
    parser.add_argument('--steps', type=int, default=256)
    parser.add_argument('--temperature', type=float, default=1.0)
    parser.add_argument('--topp', type=float, default=0.9)
    args = parser.parse_args()
    try:
        text = generate(args.prompt, args.checkpoint, args.steps,
                        args.temperature, args.topp)
        print(text)
    except Exception as e:
        logger.error('Generation failed: %s', e)

