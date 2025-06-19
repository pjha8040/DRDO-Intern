#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define n 624
#define m 397
#define w 32
#define r 31
#define UMASK (0xffffffffUL << r)
#define LMASK (0xffffffffUL >> (w-r))
#define a 0x9908b0dfUL
#define u 11
#define s 7
#define t 15
#define l 18
#define b 0x9d2c5680UL
#define c 0xefc60000UL
#define f 1812433253UL

typedef struct {
    uint32_t state_array[n];
    int state_index;
} mt_state;

void initialize_state(mt_state* state, uint32_t seed) {
    state->state_array[0] = seed;
    for (int i = 1; i < n; i++) {
        seed = f * (seed ^ (seed >> (w - 2))) + i;
        state->state_array[i] = seed;
    }
    state->state_index = 0;
}

uint32_t random_uint32(mt_state* state) {
    uint32_t* state_array = state->state_array;
    int k = state->state_index;
    int j = k - (n - 1);
    if (j < 0) j += n;

    uint32_t x = (state_array[k] & UMASK) | (state_array[j] & LMASK);
    uint32_t xA = x >> 1;
    if (x & 1UL) xA ^= a;

    j = k - (n - m);
    if (j < 0) j += n;

    x = state_array[j] ^ xA;
    state_array[k++] = x;
    if (k >= n) k = 0;
    state->state_index = k;

    uint32_t y = x ^ (x >> u);
    y ^= (y << s) & b;
    y ^= (y << t) & c;
    uint32_t z = y ^ (y >> l);

    return z;
}

void write_random_bits_to_file(const char* filename, int total_bits) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        perror("File opening failed");
        exit(1);
    }

    mt_state mt;
    initialize_state(&mt, 5489UL);  // example seed

    int bits_written = 0;
    while (bits_written < total_bits) {
        uint32_t num = random_uint32(&mt);
        for (int i = 31; i >= 0 && bits_written < total_bits; i--) {
            char bit = ((num >> i) & 1) ? '1' : '0';
            fputc(bit, fp);
            bits_written++;
        }
    }

    fclose(fp);
    printf("Generated %d bits and saved to '%s'\n", total_bits, filename);
}

int main() {
    write_random_bits_to_file("random_bits.txt", 100000);  // 1e5 bits
    return 0;
}
