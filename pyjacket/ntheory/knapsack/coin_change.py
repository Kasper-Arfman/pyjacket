q = None


def can_change(coins=None, target=None) -> bool:
    """Determine if I can match a target price with the given coins.
    
    Recursive approach that may perform redundant computations.
    """

    def recurse(target: int, coins: list):
        print(f"trying {target = } {coins = }")
        
        if target == 0:
            return True
            
        for c in coins:
            t = target - c                
            if recurse(t, coins=[x for x in coins if 0<x<=t and x!=c]):
                return True
                
        return False
            
    return recurse(
        target, 
        coins=sorted([c for c in coins if 0<c<=target], reverse=True)
    )
    
    
def gen_change(coins=None, target=None) -> bool:
    """Generate all ways to compose target using coins.
    
    Recursive approach that may perform redundant computations.
    """

    def recurse(target: int, coins: list, r: list):
        print(f"trying {target = } {coins = }")
        if target == 0:
            yield r
            return True
            
        for c in coins:
            t = target - c                
            yield from recurse(
                t, 
                [x for x in coins if 0<x<=t and x!=c],
                r + [c]
                )  
        return
    
    coins = CustomCounter(coins)
    
    for c in coins:
        if not 0<c<=target:
            del coins[c]
    
            
    return list(recurse(
        target, 
        coins=sorted([c for c in coins if 0<c<=target], reverse=True),
        r=[]
    ))
    




q = gen_change(
    coins = [2, 3, 5, 6, 10, 13, 20, 50],
    target = 37,   
)







print(q)