import os
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

def runs_test(binary_data):
    """Performs NIST Runs Test on binary string."""
    n = len(binary_data)
    pi = binary_data.count('1') / n

    if abs(pi - 0.5) >= (2 / n) ** 0.5:
        return [n, binary_data.count('1'), binary_data.count('0'), "-", "-", "FAIL (pi too far from 0.5)"]

    # Count number of runs
    Vn = 1
    for i in range(1, n):
        if binary_data[i] != binary_data[i - 1]:
            Vn += 1

    p_value = erfc(abs(Vn - 2 * n * pi * (1 - pi)) / (2 * (2 * n) ** 0.5 * pi * (1 - pi)))
    result = "PASS" if p_value >= 0.01 else "FAIL"

    return [n, binary_data.count('1'), binary_data.count('0'), Vn, round(p_value, 6), result]

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
            test_result = runs_test(binary_data)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Count of 1s", "Count of 0s", "Runs (Vn)", "P-Value", "Result"]
    print("\n📊 Runs Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
