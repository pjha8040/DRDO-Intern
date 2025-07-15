import os
import math
from tabulate import tabulate
from scipy.special import gammaincc

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

def longest_run_ones_in_block_test(binary_data, M=128):
    """Performs the Longest Run of Ones in a Block Test."""
    n = len(binary_data)
    K = 3  # number of degrees of freedom
    N = n // M  # number of blocks

    if N == 0:
        return [n, "-", "-", "-", "-", "FAIL (Insufficient data)"]

    blocks = [binary_data[i * M:(i + 1) * M] for i in range(N)]

    # Count max run lengths
    def max_run_of_1s(block):
        return max(len(run) for run in block.split('0'))

    v = [0] * 4  # Categories: ≤4, 5–6, 7–8, ≥9
    for block in blocks:
        r = max_run_of_1s(block)
        if r <= 4:
            v[0] += 1
        elif r <= 6:
            v[1] += 1
        elif r <= 8:
            v[2] += 1
        else:
            v[3] += 1

    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    chi_squared = sum(((v[i] - N * pi[i]) ** 2) / (N * pi[i]) for i in range(4))
    p_value = gammaincc(K / 2, chi_squared / 2)
    result = "PASS" if p_value >= 0.01 else "FAIL"

    return [n, N, v, round(chi_squared, 4), round(p_value, 6), result]

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
            test_result = longest_run_ones_in_block_test(binary_data)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Block Count (N)", "Category Counts [≤4,5–6,7–8,≥9]", "Chi²", "P-Value", "Result"]
    print("\n📊 Longest Run of 1s in Block Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
