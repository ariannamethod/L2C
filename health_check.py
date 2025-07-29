import time
import math
import logging
from l2c import generate

logger = logging.getLogger(__name__)


def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    total = len(text)
    return -sum((c / total) * math.log2(c / total) for c in freq.values())


def check():
    start = time.time()
    try:
        out = generate('', steps=8)
        available = True
    except Exception as e:
        logger.error('Health check generation failed: %s', e)
        available = False
        out = ''
    duration = time.time() - start
    speed = len(out) / duration if duration else 0.0
    entropy = shannon_entropy(out)
    return {'available': available, 'speed_chars_per_s': speed, 'entropy': entropy}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    metrics = check()
    for k, v in metrics.items():
        print(f'{k}: {v}')

