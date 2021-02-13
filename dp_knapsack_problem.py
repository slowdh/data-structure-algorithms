def get_optimal_knapsack(item_lst, capacity):
    memo = [[0 for _ in range(len(item_lst) + 1)] for _ in range(capacity + 1)]
    for i in range(1, capacity + 1):
        for j in range(1, len(item_lst) + 1):
            new_capacity = i - item_lst[j-1][1]
            if new_capacity < 0:
                memo[i][j] = memo[i][j-1]
            else:
                memo[i][j] = max(memo[i][j-1], memo[i - item_lst[j-1][1]][j-1] + item_lst[j-1][0])
    optimal_value = memo[capacity][len(item_lst)]

    lst_choices = []
    capa_curr = capacity
    for item_curr in range(len(item_lst), -1, -1):
        new_capa = capa_curr - item_lst[item_curr - 1][1]
        exclude = memo[capa_curr][item_curr - 1]
        include = memo[capa_curr - item_lst[item_curr - 1][1]][item_curr - 1] + item_lst[item_curr - 1][0] if new_capa >= 0 else 0
        if include > exclude:
            lst_choices.append(item_lst[item_curr - 1])
            capa_curr = new_capa
    return (optimal_value, lst_choices)


capacity = 6
# (value, size)
item_lst = [(3, 4), (2, 3), (4, 2), (4, 3)]
print(get_optimal_knapsack(item_lst=item_lst, capacity=capacity))