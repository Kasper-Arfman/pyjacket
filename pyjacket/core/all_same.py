

def all_same(arr):
    if arr==[]: return True
    x0 = arr[0]
    return all(
        (x==x0) for x in arr[1:]
    )
    