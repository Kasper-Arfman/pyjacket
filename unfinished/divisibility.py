if __name__ == '__main__': 
    import sys; sys.path.append(r'C:\Users\Kasper\Documents\GitHub\kaspy')
    
import kaspy


def digits(n):
    return [int(d) for d in str(n)]


def digital_sum(n):
    return sum(digits(n))

def digital_root(n):
    if n < 10:
        return n
    
    return digital_root(digital_sum(n))




def div3(n):
    """A num is divisible by 3 if and only if the sum of its digits is divisible by 3"""
    return digital_sum(n) % 3 == 0

def div9(n):
    return digital_sum(n) % 9 == 0


if __name__ == '__main__':


    q = None


    q = div3(111)
    q = div3(215)
    q = div3(327)



    print(q)