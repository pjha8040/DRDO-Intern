import math
from scipy.stats import norm

def non_overlapping_template_test(bits, template='000', block_size=1032):
    m = len(template)
    n = len(bits)

    if block_size <= m:
        raise ValueError("Block size must be greater than template length")
    if n < block_size:
        raise ValueError("Bit string too short for the given block size")

    num_blocks = n // block_size
    blocks = [bits[iblock_size:(i+1)block_size] for i in range(num_blocks)]

    counts = []
    for block in blocks:
        count = 0
        i = 0
        while i <= block_size - m:
            if block[i:i+m] == template:
                count += 1
                i += m 
            else:
                i += 1
        counts.append(count)

    mean = (block_size - m + 1) / (2  m)
    var = block_size * ((1 / (2  m)) - ((2 * m - 1) / (2  (2 * m))))
    chi_squared = sum([(x - mean)  2 for x in counts]) / var
    p_value = norm.sf(math.sqrt(chi_squared)) * 2  

    print(f"[Non-Overlapping Template Test] template = '{template}', p-value = {p_value:.6f}")
    return p_value >= 0.01