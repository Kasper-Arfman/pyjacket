


def is_prime(n):
    if n<2 or (n > 2 and n & 1 == 0):
        return False
    
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True




if __name__ == '__main__':
    
    for x in range(15):
        print(x, is_prime(x))