# def digits(num, base=10):
#     if num == 0:
#         return [0]
    
#     if base == 10:
#         return list(map(int, str(num)))
    
#     else:
#         digits = []
#         while num:
#             digits.append(int(num % base))
#             num //= base
#         return digits[::-1]
    
    
def digits(n, base=10):
    if base<=1: raise ValueError(f"Base must be greater than 1, got {base}")
    # elif base == 2: ...
    elif base == 10:  return [int(x) for x in str(n)]
    
    digits = []
    while n > 0:
        n, r = divmod(n, base)
        digits.insert(0, r)
    return digits
        

# q = digits(110, base=2)
# print(q)



