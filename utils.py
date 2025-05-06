def ease_out_cubic(t):
    return 1 - (1 - t)**3

def ease_out_sine(t):
    from math import sin, pi
    return sin((t * pi) / 2)
