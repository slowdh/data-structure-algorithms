import time

def get_max_weighted_independent_set_recursion(path_weight_array, end=None):
    if end is None:
        end = len(path_weight_array) - 1
    if end == 0:
        return path_weight_array[0]
    elif end == 1:
        return max(path_weight_array[:2])
    return max(get_max_weighted_independent_set_recursion(path_weight_array, end=end-2) + path_weight_array[end], get_max_weighted_independent_set_recursion(path_weight_array, end=end-1))

def get_max_weighted_independent_set_dp(path_weight_array):
    memo = []
    memo.append(path_weight_array[0])
    memo.append(max(path_weight_array[:2]))
    for i in range(2, len(path_weight_array)):
        memo.append(max(memo[i-2] + path_weight_array[i], memo[i-1]))
    return memo[-1]


# len(input_arr) == 30
input_arr = [5, 99, 100, 99, 7, 8, 12, 123, 96, 12] * 3

recursion_before = time.time()
get_max_weighted_independent_set_recursion(input_arr)
recursion_after = dp_before = time.time()
get_max_weighted_independent_set_dp(input_arr)
dp_after = time.time()
ratio = (recursion_after - recursion_before) / (dp_after - dp_before)

print(f'DP version executed {ratio} times faster!')
# DP version executed 27651.11111111111 times faster!


