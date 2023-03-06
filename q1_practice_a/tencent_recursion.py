def f(x, target):
    if len(x) == 1:
        return abs(x[0]) == abs(target)
    
    return f(x[1:],target-x[0]) or f(x[1:], target + x[0])
