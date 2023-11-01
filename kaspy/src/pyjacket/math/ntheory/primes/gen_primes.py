from typing import Dict

def gen_primes():
    composites: Dict[int, list] = {}  # map composite number to its prime factors
    num = 2  # let 2 be the first prime number
    while True:
        if num in composites:
            for factor in composites[num]:
                # num is composite so we write it as:
                # num = k * factor
                
                # Mark the next composite number of the given factor:
                # next = (k+1) * factor
                #      =   num + factor
                next_composite = factor + num
                composites[next_composite] = composites.get(next_composite, []) + [factor]
                
            # we can forget about numbers we have crossed
            del composites[num]
    
        else:
            yield num
            composites[num * num] = [num]  # mark q^2 to be composite
            
