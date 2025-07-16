import math
from scipy.special import erfc

def runs_test(bits):
    n = len(bits)
    pi = bits.count('1') / n
    if abs(pi - 0.5) >= (2 / math.sqrt(n)):
        print("[Runs Test] Fails proportion condition.")
        return False

    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1

    expected_runs = 2 * n * pi * (1 - pi)
    variance = 2 * n * pi * (1 - pi) * (2 * pi * (1 - pi) - 1)
    z = abs(runs - expected_runs) / math.sqrt(2 * n * pi * (1 - pi))
    p_value = erfc(z / math.sqrt(2))

    print(f"[Runs Test] runs = {runs}, expected = {expected_runs:.2f}, p-value = {p_value:.6f}")
    return p_value >= 0.01
