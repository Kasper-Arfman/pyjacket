def circular_permutations(arr):
    for i in range(len(arr)):
        yield arr[i:] + arr[:i]