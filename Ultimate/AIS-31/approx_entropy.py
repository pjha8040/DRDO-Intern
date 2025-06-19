import math
from scipy.special import gammaincc

def approximate_entropy_test(bits, m=2):
    n = len(bits)
    def get_freq(m):
        freq = {}
        extended_bits = bits + bits[:m-1]  # wrap around
        for i in range(n):
            pattern = extended_bits[i:i+m]
            freq[pattern] = freq.get(pattern, 0) + 1
        return freq

    freq_m   = get_freq(m)
    freq_m1  = get_freq(m+1)

    def phi(freq, m):
        total = sum(freq.values())
        return sum((count / total) * math.log(count / total) for count in freq.values())

    phi_m   = phi(freq_m, m)
    phi_m1  = phi(freq_m1, m+1)

    ap_en = phi_m - phi_m1
    chi_squared = 2 * n * (math.log(2) - ap_en)
    df = 2 ** (m - 1)
    p_value = gammaincc(df, chi_squared / 2)

    print(f"[Approximate Entropy Test] ApEn = {ap_en:.6f}, p-value = {p_value:.6f}")
    return p_value >= 0.01
