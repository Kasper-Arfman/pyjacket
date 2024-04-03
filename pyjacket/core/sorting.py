def sortby(X, Y):
    return [x for (_, x) in sorted(zip(Y, X), key=lambda pair: pair[0])] 