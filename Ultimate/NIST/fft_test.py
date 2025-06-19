import numpy as np
from scipy.special import erfc
import math

def dft_test(bits):
    n = len(bits)
    X = np.array([1 if b == '1' else -1 for b in bits])

    # Step 2: Compute DFT and get magnitude
    S = np.fft.fft(X)
    M = np.abs(S[:n // 2])  # Only first n/2 components

    # Step 3: Compute threshold
    T = math.sqrt(math.log(1 / 0.05) * n)

    # Step 4: Count the peaks less than T
    N0 = 0.95 * n / 2
    N1 = np.sum(M < T)

    # Step 5: Compute d
    d = (N1 - N0) / math.sqrt(n * 0.95 * 0.05 / 4)

    # Step 6: Compute p-value
    p_value = erfc(abs(d) / math.sqrt(2))

    print(f"[DFT Test] N1 = {N1}, N0 = {N0:.2f}, d = {d:.4f}, p-value = {p_value:.6f}")
    return p_value >= 0.01  # Passes if p-value ≥ 0.01