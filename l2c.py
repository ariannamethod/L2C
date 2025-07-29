import ctypes
import os
import json
import hashlib
import datetime
import logging

logger = logging.getLogger(__name__)

_lib = None

DATASET_DIR = "datasets"
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "train_log.json")
MAX_DATASET_SIZE = 5 * 1024 * 1024  # 5MB


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


def compute_sha256(path: str) -> str:
    """Return SHA-256 hash of file at ``path``."""
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _load_train_log(log_path: str = LOG_FILE) -> list:
    if not os.path.exists(log_path):
        return []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:  # pylint: disable=broad-except
        logger.warning('Failed to read %s', log_path)
    return []


def _write_train_log(entries: list, log_path: str = LOG_FILE) -> None:
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2)


def _needs_training(entries: list, filename: str, sha256: str) -> bool:
    for e in entries:
        if e.get('filename') == filename and e.get('sha256') == sha256:
            return False
    return True


def check_dataset_updates(dataset_dir: str = DATASET_DIR,
                          log_path: str = LOG_FILE):
    """Return list of dataset paths needing training and existing log entries."""
    entries = _load_train_log(log_path)
    datasets = []
    for item in os.scandir(dataset_dir):
        if not item.is_file() or not item.name.lower().endswith('.bin'):
            continue
        if os.path.getsize(item.path) > MAX_DATASET_SIZE:
            logger.warning('%s exceeds size limit and will be ignored', item.name)
            continue
        sha256 = compute_sha256(item.path)
        if _needs_training(entries, item.name, sha256):
            datasets.append((item.path, item.name, sha256))
    return datasets, entries


def auto_train(dataset_dir: str = DATASET_DIR, log_path: str = LOG_FILE) -> None:
    """Automatically tokenize and train on new datasets."""
    datasets, entries = check_dataset_updates(dataset_dir, log_path)
    for path, name, sha256 in datasets:
        tokenize_file(path)
        train(path)
        entries.append({
            'filename': name,
            'sha256': sha256,
            'trained_at': datetime.datetime.utcnow().isoformat()
        })
    if datasets:
        _write_train_log(entries, log_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auto_train()



