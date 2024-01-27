



def div2(n):
    return not n & 1


def div3(n):
    """The sum of its digits must be divisible by 3"""    
    while n > 10:
        n = sum(map(int, str(n)))
    return n % 3 == 0


def div5(n):
    return str(n)[-1] in '05'


def div7(n):
    pass



""" 
A number is divisible by a composite number if it is divisible by all of the prime factors


"""