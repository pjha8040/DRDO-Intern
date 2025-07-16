import os
import numpy as np
from tabulate import tabulate
from scipy.special import gammaincc

def read_binary_file(file_path):
    """Reads a file containing raw binary bits (0s and 1s) as a string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        data = f.read()

    binary_data = ''.join(filter(lambda x: x in '01', data))
    if len(binary_data) == 0:
        raise ValueError("No binary data found in the file.")
    return binary_data

def serial_test(binary_data, m=3):
    """Performs the Serial Test as per NIST SP 800-22."""
    n = len(binary_data)
    if n < 1000:
        return [n, "-", "-", "-", "-", "FAIL (Insufficient data)"]

    def psi2(m):
        padded_data = binary_data + binary_data[:m - 1]
        counts = [0] * (2 ** m)
        for i in range(n):
            pattern = padded_data[i:i + m]
            idx = int(pattern, 2)
            counts[idx] += 1
        return sum(count ** 2 for count in counts) * (2 ** m) / n - n

    psi_m = psi2(m)
    psi_m1 = psi2(m - 1)
    psi_m2 = psi2(m - 2)

    delta1 = psi_m - psi_m1
    delta2 = psi_m - 2 * psi_m1 + psi_m2

    p1 = gammaincc(2 ** (m - 1) / 2, delta1 / 2)
    p2 = gammaincc(2 ** (m - 2) / 2, delta2 / 2)

    result = "PASS" if p1 >= 0.01 and p2 >= 0.01 else "FAIL"

    return [n, m, round(delta1, 6), round(p1, 6), round(p2, 6), result]

def main():
    files = {
        "1MB QRNG (txt)": "qrng_1mb.txt",
        "10MB QRNG (txt)": "qrng_10mb.txt",
        "100MB QRNG (dat)": "qrng_100mb.dat"
    }

    results = []
    for label, path in files.items():
        try:
            binary_data = read_binary_file(path)
            test_result = serial_test(binary_data, m=3)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Block Size (m)", "Δ1 = ψm−ψm−1", "P1", "P2", "Result"]
    print("\n📊 Serial Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
