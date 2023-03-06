# Lec 11 Memorization 
# keep track of the computed results 
cache = {}
def fib(n):
    if n not in cache:
        if n < 2:
            cache[n] = n
        else:
            cache[n] = fib(n-1) + fib(n-2)
    return cache[n]


def prod(*numbers):
    # *args -> came in as a tuple of arguments 
    # prod(7, 8, 9) -> (7, 8, 9)
    out = 1 
    for num in numbers:
        out *= num
    return out 

# takes each of the elements in x, and pass them in as separate arguments
def prod(x, y):
    return x * y
x = [7, 8]
print(prod(*x))

y = [ 9, *x, 6]


# unexpose cache 
class MemorizedFunction:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

fib = MemorizedFunction(fib)

# using the idea of closure 
def memorized(func):
    cache = {}
    def _mfunc(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return _mfunc

fib = memorized(fib) # don't have access to cache 

# but what about this
fib2 = memorized(fib) # will be recursively calling fib and not the memorized function

