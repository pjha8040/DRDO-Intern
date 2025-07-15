import os
import numpy as np
from tabulate import tabulate
from scipy.special import erfc

def read_binary_file(file_path):
    """Reads a file containing raw binary bits (0s and 1s) as a string."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        data = f.read()

    # Clean and filter: allow only '0' and '1'
    binary_data = ''.join(filter(lambda x: x in '01', data))

    if len(binary_data) == 0:
        raise ValueError("No binary data found in the file.")
    return binary_data

def maurer_test(binary_data, L=7):
    """
    Performs Maurer's Universal Statistical Test.
    L = block size (typically 6–16). Recommended L = 7 for shorter sequences.
    """
    n = len(binary_data)
    Q = 10 * (2 ** L)  # Initialization blocks
    K = (n // L) - Q   # Test blocks

    if K <= 0:
        return [n, "-", "-", "-", "-", "FAIL (Too short for given L)"]

    # Create table T to store last occurrence of each pattern
    T = [0] * (2 ** L)
    blocks = [int(binary_data[i:i + L], 2) for i in range(0, n - L + 1, L)]

    # Initialization
    for i in range(Q):
        T[blocks[i]] = i + 1

    # Compute the test statistic
    sum_log = 0.0
    for i in range(Q, Q + K):
        pattern = blocks[i]
        last_occurrence = T[pattern]
        if last_occurrence != 0:
            distance = i + 1 - last_occurrence
            sum_log += np.log2(distance)
        else:
            sum_log += np.log2(i + 1)
        T[pattern] = i + 1

    fn = sum_log / K

    # Expected value and variance for given L (from NIST)
    expected_values = {
        6: (5.2177052, 2.954), 7: (6.1962507, 3.125),
        8: (7.1836656, 3.238), 9: (8.1764248, 3.311),
        10: (9.1723243, 3.356), 11: (10.170032, 3.384),
        12: (11.168765, 3.401), 13: (12.168070, 3.410),
        14: (13.167693, 3.416), 15: (14.167488, 3.419),
        16: (15.167379, 3.421)
    }

    if L not in expected_values:
        return [n, "-", "-", "-", "-", "FAIL (Unsupported L value)"]

    expected, variance = expected_values[L]
    sigma = np.sqrt(variance / K)
    p_value = erfc(abs(fn - expected) / (np.sqrt(2) * sigma))
    result = "PASS" if p_value >= 0.01 else "FAIL"

    return [n, L, round(fn, 6), round(expected, 6), round(p_value, 6), result]

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
            test_result = maurer_test(binary_data, L=7)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Block Size (L)", "Fn (Entropy)", "Expected", "P-Value", "Result"]
    print("\n📊 Maurer's Universal Statistical Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
