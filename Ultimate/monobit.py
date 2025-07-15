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

def monobit_test(binary_data):
    """Performs NIST Monobit Frequency Test on binary string."""
    n = len(binary_data)
    ones = binary_data.count('1')
    zeros = binary_data.count('0')
    s = sum(1 if bit == '1' else -1 for bit in binary_data)

    s_obs = abs(s) / (n  0.5)
    p_value = erfc(s_obs / 2  0.5)

    result = "PASS" if p_value >= 0.01 else "FAIL"

    return [n, ones, zeros, round(s_obs, 4), round(p_value, 6), result]

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
            test_result = monobit_test(binary_data)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 6)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Count of 1s", "Count of 0s", "|S|/sqrt(n)", "P-Value", "Result"]
    print("\n📊 Monobit Frequency Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if name == "main":
    main()
