import time
import random
import heapq
import copy


def time_decorator(func):
    def wrapper(lst):
        time_before = time.time()
        ret = func(lst)
        time_after = time.time()
        time_taken = time_after - time_before
        print(f'Time for {func.__name__}: {time_taken}')
        return ret
    return wrapper

@time_decorator
def quick_sort(lst):
    def _swap(lst, left, right):
        lst[left], lst[right] = lst[right], lst[left]

    def quick_sort_helper(lst, left, right):
        if left >= right:
            return
        pivot = left
        change = left + 1
        for curr in range(left + 1, right + 1):
            if lst[pivot] >= lst[curr]:
                _swap(lst, change, curr)
                change += 1
        _swap(lst, pivot, change - 1)

        quick_sort_helper(lst, left, change - 2)
        quick_sort_helper(lst, change, right)
        return lst
    return quick_sort_helper(lst, 0, len(lst) - 1)

@time_decorator
def merge_sort(lst):
    def merge_sort_helper(lst):
        if len(lst) <= 1:
            return lst
        half = len(lst) // 2
        left_sorted = merge_sort_helper(lst[:half])
        right_sorted = merge_sort_helper(lst[half:])
        merged = []
        while len(left_sorted) != 0 and len(right_sorted) != 0:
            if left_sorted[0] < right_sorted[0]:
                merged.append(left_sorted.pop(0))
            else:
                merged.append(right_sorted.pop(0))
        merged += left_sorted + right_sorted
        return merged
    return merge_sort_helper(lst)

@time_decorator
def bubble_sort(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] > lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst

@time_decorator
def selection_sort(lst):
    for i in range(len(lst)):
        min_val = lst[i]
        min_idx = i
        for j in range(i, len(lst)):
            if lst[j] < min_val:
                min_val = lst[j]
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst

@time_decorator
def heap_sort(lst):
    ret = []
    heapq.heapify(lst)
    for _ in range(len(lst)):
        ret.append(heapq.heappop(lst))
    return ret


lst_input = [random.randrange(100000) for _ in range(10000)]
heap_sort(copy.deepcopy(lst_input))
merge_sort(lst_input)
quick_sort(lst_input)
selection_sort(lst_input)
bubble_sort(lst_input)

"""
Time for heap_sort: 0.004563808441162109
Time for merge_sort: 0.04018521308898926
Time for quick_sort: 0.027165889739990234
Time for selection_sort: 2.574414014816284
Time for bubble_sort: 3.33627986907959
"""