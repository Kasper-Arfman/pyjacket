""" Produce all number in the set ax + by in increasing order"""

from gcd_extended import diophantine


def critical_multiple(coins):
    b, a = sorted(coins)

    # Calculate the displacement vectors for increasing the amount by 1
    (x, y), (dx, dy) = diophantine(a, b, 1)
    # forward = back[0] + shift[0], back[1] + shift[1]

    while x < 0:
        x += dx
        y += dy


    while x > 0:
        x -= dx
        y -= dy


    back = x, y

    forward = (x+dx, y+dy) if dx > 0 else (x-dx, y-dy)








    print('fw', forward)
    print('bk', back)
    # print('sh', shift)


    # compute the lowest number that can be reached using these vectors
    s1 = back[0]**2 + back[1]**2
    s2 = forward[1]**2 + forward[1]**2
    vector = back if s1 > s2 else forward
    other = back if s1 < s2 else forward

    print(vector)

    # Compute the start given a vector
    x, y = vector
    x = -min(0, x)
    y = -min(0, y)
    x0, y0 = x, y
    # print('x0,', x0, y0)

    # See if we can go back even more using other
    x, y = other
    while x0 >= 0 and y0 >= 0:
        x0 -= x
        y0 -= y
    x0 += x
    y0 += y


    # print('nudged', x0, y0)


    r = x0 * a + y0 * b
    # print(r)
    return r



if __name__ == "__main__":
    q = critical_multiple([9, 14])

    # assert critical_multiple([3, 5]) == 8
    # assert critical_multiple([4, 7]) == 18
    # # assert critical_multiple([5, 15]) == -1
    # assert critical_multiple([9, 14]) == 104

    print(q)