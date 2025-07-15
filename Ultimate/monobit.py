import os
from tabulate import tabulate
from scipy.special import erfc

def read_binary_file(file_path):
    """Reads a binary file and returns a string of bits ('0'/'1')."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        data = f.read()
    if not data:
        raise ValueError("File is empty or not readable.")
    # Convert each byte to 8-bit binary and join
    bit_str = ''.join(f"{byte:08b}" for byte in data)
    return bit_str

def monobit_test(binary_data):
    n = len(binary_data)
    ones = binary_data.count('1')
    zeros = binary_data.count('0')
    s = ones - zeros
    s_obs = abs(s) / (n ** 0.5)
    p_value = erfc(s_obs / (2 ** 0.5))
    result = "PASS" if p_value >= 0.01 else "FAIL"
    return [n, ones, zeros, round(s_obs, 4), round(p_value, 6), result]

def main():
    files = {
        "1MB QRNG (dat)": "qrng_1mb.dat",
        "10MB QRNG (dat)": "qrng_10mb.dat",
        "100MB QRNG (dat)": "qrng_100mb.dat"
    }
    results = []
    for label, path in files.items():
        try:
            bits = read_binary_file(path)
            results.append([label] + monobit_test(bits))
        except Exception as e:
            print(f"❌ Error processing {label}: {e}")
            results.append([label] + ["ERROR"] * 6)
    headers = ["File", "Total Bits", "Count of 1s", "Count of 0s", "|S|/√n", "P-Value", "Result"]
    print("\nMonobit Frequency Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
