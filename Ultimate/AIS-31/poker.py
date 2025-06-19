import math
from scipy.stats import chi2

def poker_test(bits, m=4):
    n = len(bits)
    if n < m or n % m != 0:
        raise ValueError("Bit string length must be divisible by m")

    k = n // m
    patterns = {}

    for i in range(0, n, m):
        pattern = bits[i:i + m]
        patterns[pattern] = patterns.get(pattern, 0) + 1

    sum_sq = sum(count2 for count in patterns.values())
    X = ((2*m) / k) * sum_sq - k
    df = (2**m) - 1
    p_value = chi2.sf(X, df)

    print(f"[Poker Test] chi2 = {X:.4f}, p-value = {p_value:.6f}")
    return p_value >= 0.01
