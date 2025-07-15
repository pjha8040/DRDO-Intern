def long_run_test(binary_data, threshold=34):
    """AIS-31 Long Run Test: Detects if any single run exceeds the threshold."""
    n = len(binary_data)
    if n < 100:
        return [n, "-", "FAIL (Too short)"]

    max_run = 1
    current_run = 1

    for i in range(1, n):
        if binary_data[i] == binary_data[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    result = "PASS" if max_run <= threshold else "FAIL"
    return [n, max_run, threshold, result]

def run_long_run_test_on_files():
    files = {
        "1MB QRNG (txt)": "qrng_1mb.txt",
        "10MB QRNG (txt)": "qrng_10mb.txt",
        "100MB QRNG (dat)": "qrng_100mb.dat"
    }

    results = []
    for label, path in files.items():
        try:
            binary_data = read_binary_file(path)
            test_result = long_run_test(binary_data, threshold=34)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 4)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Max Run Length", "Threshold", "Result"]
    print("\n🧬 AIS-31 Long Run Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

# Usage
if __name__ == "__main__":
    run_long_run_test_on_files()
