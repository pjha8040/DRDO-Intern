from itertools import permutations
from collections import Counter
from read_byte_file import read_byte_file
import os

def read_byte_file(file_path):
    """Reads file in binary mode and returns list of byte values (0–255)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        byte_data = list(f.read())

    if len(byte_data) == 0:
        raise ValueError("No byte data found in the file.")
    return byte_data


def overlapping_permutation_test(byte_data, tuple_size=5):
    max_index = len(byte_data) - tuple_size
    tuples = [tuple(byte_data[i:i + tuple_size]) for i in range(max_index)]
    perms = [tuple(sorted(t)) for t in tuples]

    perm_freq = Counter(perms)
    expected = len(perms) / len(set(perms))
    chi_square = sum((f - expected)**2 / expected for f in perm_freq.values())
    result = "PASS" if chi_square < 500 else "FAIL"
    return len(perms), round(chi_square, 2), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    total, chi, result = overlapping_permutation_test(byte_data)
    print(f"🔄 Diehard Overlapping Permutation Test — {file_path}")
    print(f"Permutations: {total} | Chi²: {chi} | Result: {result}")

if __name__ == "__main__":
    main()
