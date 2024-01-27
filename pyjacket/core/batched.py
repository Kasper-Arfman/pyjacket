

x = int(5)
x.__xor__(y)


def batched(iterable, n):
    """Expects iterable length to be multiple of input"""
    N = len(iterable)
    for i in range(0, N, n):
        yield iterable[i:i+n] 
        
        
def zipped(iterable, n):
    N = len(iterable)
    for i in range(0, N):
        yield iterable[i: i+n]
    

 def zipped(iterable, n):
    iterable = iter(iterable)
    v = tuple(next(iterable) for _ in range(n))
    yield v
    for e in iterable:
        v = (*v[1:], e)
        yield v       
    
    
# x = [1, 2, 3, 4, 5, 6]
# q = list(batched(x, 2))
# print(q)
y = [0, 1, 2, 3, 4, 5, 6]
for x in zipped(y, 3):
    print(x)