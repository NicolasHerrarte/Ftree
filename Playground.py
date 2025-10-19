def bezout_next(previous, current, direction):
    multiplier = previous[direction]
    swap_coefs = [x*multiplier for x in current]
    coefs = [0,0]
    coefs[not direction] = swap_coefs[1]+previous[not direction]
    coefs[direction] = swap_coefs[0]
    return tuple(coefs)

f = bezout_next((5, 2), (1, 2), False)
print(f)
