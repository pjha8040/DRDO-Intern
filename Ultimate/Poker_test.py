import os
from collections import Counter
from tabulate import tabulate
from scipy.stats import chi2

def read_binary_file(file_path):
    """Reads and filters binary string from file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        data = f.read()
    binary_data = ''.join(filter(lambda x: x in '01', data))
    if not binary_data:
        raise ValueError("No binary data found.")
    return binary_data

def poker_test(binary_data, m=4):
    """AIS-31 Poker Test."""
    n = len(binary_data)
    if n < m * 5:
        return [n, "-", "-", "-", "FAIL (Data too short)"]

    k = n // m
    blocks = [binary_data[i*m:(i+1)*m] for i in range(k)]
    counts = Counter(blocks)
    X = (2 ** m / k) * sum(f ** 2 for f in counts.values()) - k

    p_value = 1 - chi2.cdf(X, df=(2 ** m - 1))
    result = "PASS" if p_value >= 0.01 else "FAIL"
    return [n, m, k, round(X, 4), round(p_value, 6), result]

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
            test_result = poker_test(binary_data, m=4)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Block Size (m)", "Block Count (k)", "Chi²", "P-Value", "Result"]
    print("\n🎲 AIS-31 Poker Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
