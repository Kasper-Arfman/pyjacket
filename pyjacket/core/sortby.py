def sortby(X, Y):
    return [x for (y,x) in sorted(zip(Y,X), key=lambda pair: pair[0])] 





x = 'abfedc'

y = [1, 2, 3, 4, 5, 6]


y = sortby(y, x)

print(y)