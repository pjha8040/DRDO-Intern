import math
from collections import Counter

def block_entropy_estimation(binary_data, block_size=8):
    """Estimates the Shannon entropy per bit in the binary data."""
    n = len(binary_data)
    if n < block_size * 100:
        return [n, "-", "-", "FAIL (Too short)"]

    # Split into blocks
    num_blocks = n // block_size
    blocks = [binary_data[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]

    freq = Counter(blocks)
    total = sum(freq.values())

    # Compute block entropy
    entropy = -sum((count / total) * math.log2(count / total) for count in freq.values())
    entropy_per_bit = entropy / block_size

    result = "PASS" if entropy_per_bit >= 0.997 else "FAIL"
    return [n, block_size, round(entropy, 6), round(entropy_per_bit, 6), result]

def run_entropy_test_on_files():
    files = {
        "1MB QRNG (txt)": "qrng_1mb.txt",
        "10MB QRNG (txt)": "qrng_10mb.txt",
        "100MB QRNG (dat)": "qrng_100mb.dat"
    }

    results = []
    for label, path in files.items():
        try:
            binary_data = read_binary_file(path)
            test_result = block_entropy_estimation(binary_data, block_size=8)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 5)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Block Size", "Entropy (bits)", "Entropy/bit", "Result"]
    print("\n🔐 AIS-31 Block Entropy Estimation Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

# Usage
if __name__ == "__main__":
    run_entropy_test_on_files()
