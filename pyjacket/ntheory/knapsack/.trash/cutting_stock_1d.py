def first_fit(order, stock_length):
    """ Solution A.
    PROs:
        - Computationally fast
        - Easy to implement
        
    CONs:
        - Does not guarantee an optimal solution
    """
    sorted_demands = sorted(order, reverse=True)
    stocks = [[]]  # list of parts 
    for length in sorted_demands:
        for stock in stocks:
            if sum(stock) + length <= stock_length:
                stock.append(length)
                break
        else:  # if 'break' is not reached
            stocks.append([length])
    return stocks


if __name__ == '__main__':
    stock_length = 8
    order = [3, 3, 3, 2, 2, 2, 2]
    result = first_fit(order, stock_length)
        
    """
    == OPTIMAL SOLUTION EXAMPLE:
     - stock length = 8
     - order = [3, 3, 3, 2, 2, 2, 2]
    1: [3, 3, 2], Remaining length: 0    
    2: [3, 2, 2], Remaining length: 1    
    3: [2], Remaining length: 6
    
    
    == SUBOPTIMAL SOLUTION EXAMPLE:
     - stock length 55
     - order [30, 24, 20, 15, 11, 10, 10]
    1: [30, 24], Remaining length: 1     
    2: [20, 15, 11], Remaining length: 9 
    3: [10, 10], Remaining length: 35
    
    (optimal solution)
    1: [30, 20, 15]    
    2: [24, 11, 10, 10]
    """
