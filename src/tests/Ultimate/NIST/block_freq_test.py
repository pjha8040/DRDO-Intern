import math
from scipy.special import gammaincc 

def block_frequency_test(bits, block_size=128):
    n = len(bits)
    if n < block_size:
        raise ValueError("Sequence length too short for given block size")

    num_blocks = n // block_size
    blocks = [bits[iblock_size:(i+1)block_size] for i in range(num_blocks)]
    proportions = [block.count('1') / block_size for block in blocks]

    chi_squared = 4 * block_size * sum((p - 0.5)**2 for p in proportions)
    p_value = gammaincc(num_blocks / 2, chi_squared / 2)

    print(f"[Block Frequency Test] chi2 = {chi_squared:.4f}, p-value = {p_value:.6f}")
    return p_value >= 0.01