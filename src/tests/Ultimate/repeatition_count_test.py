def repetition_count_test(binary_data, threshold=34):
    """AIS-31 Repetition Count Test: Fails if any repeated bit sequence exceeds threshold."""
    n = len(binary_data)
    if n < 100:
        return [n, "-", "FAIL (Too short)"]

    max_repetition = 1
    current_repetition = 1

    for i in range(1, n):
        if binary_data[i] == binary_data[i - 1]:
            current_repetition += 1
            max_repetition = max(max_repetition, current_repetition)
        else:
            current_repetition = 1

    result = "PASS" if max_repetition <= threshold else "FAIL"
    return [n, max_repetition, threshold, result]

def run_rct_on_files():
    files = {
        "1MB QRNG (txt)": "qrng_1mb.txt",
        "10MB QRNG (txt)": "qrng_10mb.txt",
        "100MB QRNG (dat)": "qrng_100mb.dat"
    }

    results = []
    for label, path in files.items():
        try:
            binary_data = read_binary_file(path)
            test_result = repetition_count_test(binary_data, threshold=34)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 4)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Max Repetition", "Threshold", "Result"]
    print("\n🔁 AIS-31 Repetition Count Test (RCT) Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

# Usage
if __name__ == "__main__":
    run_rct_on_files()
