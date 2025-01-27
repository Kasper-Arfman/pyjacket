import heapq

def count_using(input_set):
    """
    Produce all the possible numbers that may be computed from this set:
    >>> count({13, 41})
    ... [13, 26, 39, 41, 52, 54, 65, 67, ...]
    """
    # Initialize the priority queue (heap) and seen set
    heap = []
    seen = set()
    
    # Add initial elements from the input set
    for x in input_set:
        heapq.heappush(heap, x)
        seen.add(x)
    
    # Infinite generation of numbers
    while True:
        # Get the smallest number
        smallest = heapq.heappop(heap)
        yield smallest
        
        # Add new combinations with elements from the input set
        for x in input_set:
            new_sum = smallest + x
            if new_sum not in seen:
                heapq.heappush(heap, new_sum)
                seen.add(new_sum)

# Example usage
gen = count_using({3, 6})
for _, number in zip(range(20), gen):  # Limit to demonstrate the first few numbers
    print(number)