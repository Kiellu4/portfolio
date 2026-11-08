import random
from pathlib import Path


def transform(path: Path) -> None:
    data = path.read_bytes()
    key = data[:5].ljust(5, b'\x00')
    random.seed(int.from_bytes(key, 'little'))
    output = bytearray(len(data))
    for index, value in enumerate(data):
        output[index] = value ^ random.getrandbits(8)
    path.write_bytes(output)


if __name__ == '__main__':
    transform(Path('flag.txt'))
