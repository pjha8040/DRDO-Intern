import os
from read_byte_file import read_byte_file
import math

def read_byte_file(file_path):
    """Reads file in binary mode and returns list of byte values (0–255)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'rb') as f:
        byte_data = list(f.read())

    if len(byte_data) == 0:
        raise ValueError("No byte data found in the file.")
    return byte_data

def monte_carlo_pi_test(byte_data):
    if len(byte_data) < 2:
        return "N/A", "FAIL"
    pairs = zip(byte_data[::2], byte_data[1::2])
    total = 0
    inside = 0
    for x, y in pairs:
        total += 1
        norm_x = x / 255
        norm_y = y / 255
        if norm_x ** 2 + norm_y ** 2 <= 1:
            inside += 1
    pi_est = 4 * inside / total
    result = "PASS" if abs(pi_est - math.pi) <= 0.1 else "WARN"
    return round(pi_est, 5), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    pi_est, result = monte_carlo_pi_test(byte_data)
    print(f"📊 Monte Carlo π Estimation — {file_path}")
    print(f"Estimated π: {pi_est} | Result: {result}")

if __name__ == "__main__":
    main()
