import os
import math
from collections import Counter
from read_byte_file import read_byte_file

def read_byte_file(file_path):
    """Reads file in binary mode and returns list of byte values (0–255)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        byte_data = list(f.read())

    if len(byte_data) == 0:
        raise ValueError("No byte data found in the file.")
    return byte_data

def entropy_test(byte_data):
    n = len(byte_data)
    counts = Counter(byte_data)
    entropy = -sum((count / n) * math.log2(count / n) for count in counts.values())
    result = "PASS" if abs(entropy - 8.0) <= 0.1 else "WARN"
    return round(entropy, 4), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    entropy, result = entropy_test(byte_data)
    print(f"📊 Entropy Test — {file_path}")
    print(f"Entropy: {entropy} bits/byte | Result: {result}")

if __name__ == "__main__":
    main()
