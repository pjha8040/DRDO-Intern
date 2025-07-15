from scipy.special import erfc
import math
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

def bytes_to_bits(byte_data):
    """Converts list of bytes to list of bits (0 or 1)."""
    return [int(b) for byte in byte_data for b in format(byte, '08b')]

def sts_monobit(bits):
    n = len(bits)
    s = sum(1 if bit == 1 else -1 for bit in bits)
    s_obs = abs(s) / math.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))
    return round(p_value, 6), "PASS" if p_value >= 0.01 else "FAIL"

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    bits = bytes_to_bits(byte_data)
    p_val, result = sts_monobit(bits)
    print(f"🧪 Marsaglia STS Monobit Test — {file_path}")
    print(f"P-Value: {p_val} | Result: {result}")

if __name__ == "__main__":
    main()
