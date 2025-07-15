import numpy as np
import os

def bytes_to_bits(byte_data):
    """Converts list of bytes to list of bits (0 or 1)."""
    return [int(b) for byte in byte_data for b in format(byte, '08b')]

def read_byte_file(file_path):
    """Reads file in binary mode and returns list of byte values (0–255)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        byte_data = list(f.read())

    if len(byte_data) == 0:
        raise ValueError("No byte data found in the file.")
    return byte_data


def matrix_rank_test(bits, rows=32, cols=32, samples=1000):
    ranks = Counter()
    matrix_size = rows * cols
    for i in range(samples):
        segment = bits[i * matrix_size: (i + 1) * matrix_size]
        if len(segment) < matrix_size:
            break
        mat = np.array(segment).reshape((rows, cols))
        rank = np.linalg.matrix_rank(mat)
        ranks[rank] += 1

    # Expected distribution (simplified)
    full_rank_ratio = ranks[rows] / samples if samples else 0
    result = "PASS" if full_rank_ratio > 0.7 else "FAIL"
    return ranks, full_rank_ratio, result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    bits = bytes_to_bits(byte_data)
    ranks, full_ratio, result = matrix_rank_test(bits)
    print(f"🧮 Binary Matrix Rank Test — {file_path}")
    print(f"Full Rank Ratio: {round(full_ratio, 4)} | Result: {result}")
    print("Rank Distribution:", dict(ranks))

if __name__ == "__main__":
    main()
