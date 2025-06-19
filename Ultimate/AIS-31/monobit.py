import math
from scipy.special import erfc

def monobit_test(bits):
    n = len(bits)
    count = bits.count('1') - bits.count('0')
    s_obs = abs(count) / math.sqrt(n)
    p_value = erfc(s_obs / math.sqrt(2))

    print(f"[Monobit Test] s_obs = {s_obs:.4f}, p-value = {p_value:.6f}")
    return p_value >= 0.01  # True if random