def range(start, stop, step):
    if start >= stop:
        return [] 
    return [start] + range(start+step, stop, step)
    

print(range(0, 10, 1))
