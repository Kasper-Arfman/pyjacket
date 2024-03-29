import numpy as np

def primes_below(n) -> np.ndarray:
    if n < 4: return np.array([])
    
    sieve = np.ones(n//3 + (n%6==2), dtype=np.bool_)
    sieve[0] = False
    for i in range(int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)//3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))//3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]