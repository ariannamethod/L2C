import os
from datetime import datetime
from l2c import generate

OUT_DIR = 'l2c_dreams'
os.makedirs(OUT_DIR, exist_ok=True)


def dream():
    text = generate('')
    name = datetime.now().strftime('%Y%m%d_%H%M%S.txt')
    path = os.path.join(OUT_DIR, name)
    with open(path, 'w') as f:
        f.write(text)
    return path




