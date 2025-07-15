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

def spectral_test(binary_data):
    """Performs the Spectral (DFT) Test."""
    n = len(binary_data)

    if n < 1000:
        return [n, "-", "-", "-", "FAIL (Insufficient data)"]

    # Convert bits to +1/-1
    X = np.array([1 if bit == '1' else -1 for bit in binary_data])

    # Apply FFT and get magnitudes
    fft_result = np.fft.fft(X)
    modulus = np.abs(fft_result)[:n//2]

    # Threshold (95% confidence)
    T = np.sqrt(np.log(1 / 0.05) * n)
    N0 = 0.95 * (n / 2)
    N1 = np.sum(modulus < T)

    # Compute test statistic
    d = (N1 - N0) / np.sqrt(n * 0.95 * 0.05 / 4)
    p_value = erfc(abs(d) / np.sqrt(2))
    result = "PASS" if p_value >= 0.01 else "FAIL"

    return [n, int(N1), round(T, 2), round(p_value, 6), result]

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
            test_result = spectral_test(binary_data)
            results.append([label] + test_result)
        except Exception as e:
            results.append([label] + ["ERROR"] * 5)
            print(f"❌ Error processing {label}: {e}")

    headers = ["File", "Total Bits", "Peaks Below Threshold", "Threshold (T)", "P-Value", "Result"]
    print("\n📊 Spectral (Fourier Transform) Test Results")
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
