import random

def generate_prng_binary(n, seed=42):
    random.seed(seed)  
    bits = ''.join(str(random.randint(0, 1)) for _ in range(n))
    with open('2_P.txt', 'w') as f:
        f.write(bits)
    print(f"Generated PRNG binary string of length {n} and saved to pseudo-random.txt")


n = int(input("Enter number of bits to generate: "))
generate_prng_binary(n)
