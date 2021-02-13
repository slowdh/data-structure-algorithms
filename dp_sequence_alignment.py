def get_optimal_sequence_alignment(x_seq, y_seq, p_gap, p_mismatch):
    def get_mismatch_cost(char_left, char_right, p_mismatch):
        if char_left == char_right:
            return 0
        return p_mismatch

    # Setting memoization table with base case
    # Optimal_cost(i, 0) = p_gap * i
    x_len, y_len = len(x_seq), len(y_seq)
    memo = [[0 for _ in range(y_len + 1)] for _ in range(x_len + 1)]
    memo[0] = [p_gap * i for i in range(y_len + 1)]
    memo_transposed = list(map(list, zip(*memo)))
    memo_transposed[0] = [p_gap * i for i in range(x_len + 1)]
    memo = list(map(list, zip(*memo_transposed)))

    cache_choice = {}
    for i in range(1, x_len + 1):
        for j in range(1, y_len + 1):
            c0 = memo[i-1][j-1] + get_mismatch_cost(x_seq[i-1], y_seq[j-1], p_mismatch)
            c1 = memo[i-1][j] + p_gap
            c2 = memo[i][j-1] + p_gap
            minimum = min(c0, c1, c2)
            memo[i][j] = minimum
            for idx, choice in enumerate((c0, c1, c2)):
                if choice == minimum:
                    cache_choice[(i,j)] = idx

    x_optimal = y_optimal = ''
    i, j = x_len, y_len
    while i > 0 and j > 0:
        c = cache_choice[(i,j)]
        if c == 0:
            x_optimal = x_seq[i-1] + x_optimal
            y_optimal = y_seq[j-1] + y_optimal
            i -= 1
            j -= 1
        elif c == 1:
            x_optimal = x_seq[i-1] + x_optimal
            y_optimal = '-' + y_optimal
            i -= 1
        else:
            x_optimal = '-' + x_optimal
            y_optimal = y_seq[j-1] + y_optimal
            j -= 1

    len_diff = abs(i - j)
    shorter, longer = (x_optimal, y_optimal) if len(x_optimal) < len(y_optimal) else (y_optimal, x_optimal)
    shorter = '-' * len_diff + shorter
    return memo[x_len][y_len], (shorter, longer)

print(get_optimal_sequence_alignment('AGGGCT', 'AGGCA', 1, 3))
print(get_optimal_sequence_alignment('GCCTAGACGATCGGACTG', 'AGACGTGACGTGGCTGCA', 2, 1))