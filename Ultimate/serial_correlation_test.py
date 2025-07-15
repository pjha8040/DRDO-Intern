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

def serial_correlation_test(byte_data):
    n = len(byte_data)
    if n < 2:
        return "N/A", "FAIL"
    mean = sum(byte_data) / n
    numerator = sum((byte_data[i] - mean) * (byte_data[i + 1] - mean) for i in range(n - 1))
    denominator = sum((b - mean) ** 2 for b in byte_data)
    scc = numerator / denominator if denominator != 0 else 0
    result = "PASS" if abs(scc) <= 0.05 else "WARN"
    return round(scc, 6), result

def main():
    file_path = "qrng_1mb.txt"
    byte_data = read_byte_file(file_path)
    scc, result = serial_correlation_test(byte_data)
    print(f"📊 Serial Correlation Coefficient (SCC) — {file_path}")
    print(f"SCC: {scc} | Result: {result}")

if __name__ == "__main__":
    main()
