import math
from scipy.stats import chi2

def longest_run_test(bits, block_size=8):
    n = len(bits)
    if n < block_size:
        raise ValueError("Bit string too short for the given block size")

    num_blocks = n // block_size
    blocks = [bits[iblock_size:(i+1)block_size] for i in range(num_blocks)]

    max_runs = []
    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        max_runs.append(max_run)

    # Frequency of longest runs
    if block_size == 8:
        v_values = [0] * 4
        for r in max_runs:
            if r <= 1:
                v_values[0] += 1
            elif r == 2:
                v_values[1] += 1
            elif r == 3:
                v_values[2] += 1
            else:
                v_values[3] += 1
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
    else:
        raise NotImplementedError("Only block size 8 supported in this version")

    chi_squared = sum((v_values[i] - num_blocks * pi[i])*2 / (num_blocks pi[i]) for i in range(len(pi)))
    p_value = chi2.sf(chi_squared, df=len(pi) - 1)

    print(f"[Longest Run Test] chi2 = {chi_squared:.4f}, p-value = {p_value:.6f}")
    return p_value >= 0.01