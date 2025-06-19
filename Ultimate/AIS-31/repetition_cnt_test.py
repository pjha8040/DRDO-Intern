def repetition_count_test(bits, cutoff=34):
    max_run = 0
    current = 1

    for i in range(1, len(bits)):
        if bits[i] == bits[i - 1]:
            current += 1
            max_run = max(max_run, current)
        else:
            current = 1

    print(f"[Repetition Count Test] Longest run = {max_run}, Cutoff = {cutoff}")
    return max_run < cutoff  # Passes if max run < cutoff
