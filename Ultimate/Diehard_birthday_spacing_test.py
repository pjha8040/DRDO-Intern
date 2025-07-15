import random
import math
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


def birthday_spacings_test(byte_data, days=2**24, trials=512):
    birthdays = set()
    collisions = 0

    for _ in range(trials):
        bday = int.from_bytes(random.choices(byte_data, k=3), 'big') % days
        if bday in birthdays:
            collisions += 1
        birthdays.add(bday)

    expected = trials * (trials - 1) / (2 * days)
    chi_square = ((collisions - expected) ** 2) / expected if expected != 0 else 0
    result = "PASS" if chi_square < 10 else "FAIL"
    return collisions, round(chi_square, 3), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    collisions, chi, result = birthday_spacings_test(byte_data)
    print(f"Diehard Birthday Spacings Test — {file_path}")
    print(f"Collisions: {collisions} | Chi²: {chi} | Result: {result}")

if __name__ == "__main__":
    main()
