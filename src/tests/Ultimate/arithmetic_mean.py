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

def arithmetic_mean_test(byte_data):
    mean = sum(byte_data) / len(byte_data)
    result = "PASS" if abs(mean - 127.5) <= 1.0 else "WARN"
    return round(mean, 2), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    mean, result = arithmetic_mean_test(byte_data)
    print(f"📊 Arithmetic Mean Test — {file_path}")
    print(f"Mean: {mean} | Result: {result}")

if __name__ == "__main__":
    main()
