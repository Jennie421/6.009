# Lec 10

def deriv(f, dx):
    return lambda x: (f(x+dx) - f(x-dx)) / (2 * dx)

df = deriv(lambda x: 2*x**4, 0.01)

def nth_deriv(f, n, dx):
    out = f
    for _ in range(n):
        out = deriv(out, dx)
    return out

def nth_deriv(f, n, dx):
    if n == 0:
        return f
    return deriv(nth_deriv(f, n-1, dx), dx)

print(nth_deriv(lambda x: 2*x**4, 4, 1e-2)(5))


def all_caps_words(words):
    return [word.upper() for word in words]

# equivalent to looping structure
def all_caps_words(words):
    if not words:
        return []
    return [words[0].upper()] + all_caps_words(words[1:])

print(all_caps_words(['cat, dog, ferret']))

# for i in range(20):
#     print('hello', i)

def repeat(n, func):
    if n == 0:
        return 
    repeat(n-1, func)
    func(n-1)

def repeat(n, func, sofar=0):
    if n == sofar:
        return 
    func(sofar+1)
    repeat(n, func, sofar+1)

def repeat(n, func):
    def do_one_iteration(i):
        if i < n:
            func(i)
            do_one_iteration(i+1)
    do_one_iteration(0)

repeat(20, lambda i: print('hello', i))



def newtons_method_sqrt(n, epsilon):
    val = 1
    while abs(val**2 - n) > epsilon:
        print(val)
        val = (val +n/val)/2

# <initialize some variable v>
# while <condition on v>:
#     <do something>
#     <update v>

def c_style_while(initial, body, done, update):
    def helper(var):
        if done(var):
            return 
        body(var)
        helper(update(var))
    return helper(initial)

def newtons_method_sqrt(n, epsilon):
    c_style_while(
        1, 
        print,
        lambda v: abs(v**2 - n) <= epsilon,
        lambda v: (v + n/v) / 2,
    )

newtons_method_sqrt(26, 1e-6)