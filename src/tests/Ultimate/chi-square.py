from collections import Counter
from scipy.stats import chisquare
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

def chi_square_test(byte_data):
    expected = len(byte_data) / 256
    counts = [0] * 256
    for byte in byte_data:
        counts[byte] += 1
    chi_stat, p_value = chisquare(counts)
    result = "PASS" if p_value >= 0.01 else "FAIL"
    return round(chi_stat, 2), round(p_value, 6), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    chi_stat, p_value, result = chi_square_test(byte_data)
    print(f"📊 Chi-Square Test — {file_path}")
    print(f"Chi²: {chi_stat} | P-Value: {p_value} | Result: {result}")

if __name__ == "__main__":
    main()
