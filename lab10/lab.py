#!/usr/bin/env python3
"""6.009 Lab 10: Snek Interpreter Part 2"""

import sys
sys.setrecursionlimit(5000)

import doctest

###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass


class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass


class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    pass


############################
# Tokenization and Parsing #
############################


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    >>> tokenize("(foo (bar 3.14))")
    ['(', 'foo', '(', 'bar', '3.14', ')', ')']
    >>> tokenize("(cat (dog (tomato)))")
    ['(', 'cat', '(', 'dog', '(', 'tomato', ')', ')', ')']
    """
    lines = source.splitlines()
    
    exclude = {'(', ')', ' '}

    tokens = []
    for line in lines:
        line = str(line).split(';')[0] # remove comments 
        current_token = ''
        for char in line:
            if char not in exclude:
                current_token += char
            else:
                # if encountered '(', ')', ' '
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
                if not char.isspace():
                    tokens.append(char)
        
        if current_token:
            tokens.append(current_token)

    return tokens



def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    >>> parse(tokenize("(cat (dog (tomato)))"))
    ['cat', ['dog', ['tomato']]]
    >>> parse(['2'])
    2
    >>> parse(['x'])
    'x'
    >>> parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])
    ['+', 2, ['-', 5, 3], 7, 8]
    >>> parse (tokenize("(:= circle-area (function (r) (* 3.14 (* r r))))"))
    [':=', 'circle-area', ['function', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
    """

    if len(tokens) == 1:
        token = tokens[0]
        if token == '(' or token == ')':
            raise SnekSyntaxError("single input should be number or str, not {tokens}")
        answer = []
        try: 
            token = int(token)
        except: 
            try:
                token = float(token)
            except:
                pass
        return token
    
    # an expression must have ()
    if tokens[0] != '(': raise SnekSyntaxError("expression must begin with (")

    layers = [[]]

    for i, token in enumerate(tokens): # e.g. ((:= x 3)
        if token == '(':
            layers.append([]) 
        elif token == ')':
            cur_layer = layers.pop()
            if not layers:
                # if parentheses are mismatched in the input, extra ")"
                raise SnekSyntaxError("parentheses mismatched, extra ')")
            layers[-1].append(cur_layer)
        else:
            try: 
                token = int(token)
            except: 
                try:
                    token = float(token)
                except:
                    pass
            layers[-1].append(token)
    
    # if parentheses are mismatched in the input, extra "("
    if len(layers) != 1:
        raise SnekSyntaxError("parentheses mismatched, extra '('")
    
    layers = layers[0]
    
    if len(layers) == 1:
        parsed = layers[0]
    else:
        parsed = layers
    
    # check if `parsed` is valid
    def check_syntax(parsed):
        if type(parsed) != list:
            return
        if len(parsed) == 0:
            return
        
        first = parsed[0]

        if first == ':=':
            if len(parsed) != 3: 
                raise SnekSyntaxError("function define by :=: requires 3 arguments")
            # if the second element in a := statement is neither a name nor a list containing one or more parameters (strings representing paramater names).
            if not isinstance(parsed[1], str) and not isinstance(parsed[1], list): 
                raise SnekSyntaxError("function define by :=: invalid variable name")
            if not parsed[1]: 
                raise SnekSyntaxError
            # all in second element must be string
            if not all([type(i) == str for i in parsed[1]]): 
                raise SnekSyntaxError("all variable names must be strings")
            check_syntax(parsed[2])
        elif first == 'function':
            if len(parsed) != 3: 
                raise SnekSyntaxError("function define: requires 3 arguments")
            if not isinstance(parsed[1], list): 
                raise SnekSyntaxError("function define")
            if not all([isinstance(i, str) for i in parsed[1]]): 
                raise SnekSyntaxError("all variable names must be strings")
            check_syntax(parsed[2])

    check_syntax(parsed)

    # print(parsed)
    return parsed

######################
# Built-in Functions #
######################

def mul(args):
    """ return the product of all its arguments """
    out = args[0]
    for i in args[1:]:
        out *= i
    return out

def div(args):
    """ return the result of successively dividing the first argument by the remaining arguments """
    out = args[0]
    for i in args[1:]:
        out /= i
    return out

def equal(args):
    """evaluate to true if all of its arguments are equal to each other."""
    if len(args) < 2: return True
    return all([arg == args[0] for arg in args[1:]])
    # for i in args:
        # if i != args[0]:
        #     return False
    # return True 

def decrease(args):
    """ evaluate to true if its arguments are in decreasing order. """
    for i in range(len(args)-1):
        if args[i] <= args[i+1]:
            return False
    return True 

def nonincrease(args):
    """  evaluate to true if its arguments are in nonincreasing order """
    for i in range(len(args)-1):
        if args[i] < args[i+1]:
            return False
    return True 

def increase(args):
    """ evaluate to true if its arguments are in increasing order """
    for i in range(len(args)-1):
        if args[i] >= args[i+1]:
            return False
    return True 

def nondecrease(args):
    """evaluate to true if its arguments are in nondecreasing order"""
    for i in range(len(args)-1):
        if args[i] > args[i+1]:
            return False
    return True 

def _and(args, environment):
    for arg in args:
        arg = evaluate(arg, environment)
        if not arg:
            return False
    
    return True


def _or(args, environment):
    for arg in args:
        arg = evaluate(arg, environment)
        if arg:
            return True
    
    return False

def _not(arg):
    return not arg[0]

def cons(args, environment):
    """ 
    constructs new Pair object 
    before assigning the elements to car and cdr, 
    they should be evaluated in the environment in which cons is called
    """
    car = evaluate(args[0], environment)
    cdr = evaluate(args[1], environment)
    cell = Pair(car, cdr)
    return cell 


def is_type_pair(obj):
    if type(obj) == Pair:
        return True
    return False


def car(args):
    """
    take a cons cell as argument and return the first element in the pair. 
    If it is called on something that is not a cons cell, it should raise a SnekEvaluationError.
    """
    cell = args[0]
    if not is_type_pair(cell): 
        raise SnekEvaluationError("not a list of Pair objects")
    return cell.car

def cdr(args):
    """
    take a cons cell as argument and return the 2nd element in the pair. 
    If it is called on something that is not a cons cell, it should raise a SnekEvaluationError.
    """
    cell = args[0]
    if not is_type_pair(cell): raise SnekEvaluationError("not a list of Pair objects")
    return cell.cdr


def linked_list(args):
    """ This function should take zero or more arguments 
    and construct a linked list that contains those arguments, in order.
    (list) -> nil
    (list 1) -> (cons 1 nil)
    (list 1 2) -> (cons 1 (cons 2 nil))
    """
    if not args:
        return None

    return Pair(args[0], linked_list(args[1:]))


def length(args):
    """
    (length LIST) should take a list as argument and should return the length of that list. 
    When called on any object that is not a linked list, it should raise a SnekEvaluationError.
    """ 
    List = args[0]
    if List == None:
        return 0 
    if not is_type_pair(List): raise SnekEvaluationError("not Pair objects")
    if List.cdr == None:
        return 1
    return 1 + length([List.cdr])
    

def elt_at_index(args):
    """  return the element at the given index in the given list """
    List, idx = args[0], args[1]
    
    if not is_type_pair(List): raise SnekEvaluationError("not Pair objects")
    
    # If LIST is a cons cell (but not a list), then asking for index 0 should produce the car of that cons cell, and asking for any other index should raise a SnekEvaluationError
    if idx != 0: 
        if List.cdr == None:
            raise SnekEvaluationError
    elif idx == 0:
        return List.car
    return elt_at_index([List.cdr, idx-1])



def concat(args):
    """ take an arbitrary number of lists as arguments and should return a new list representing the concatenation of these lists """
    # If concat is called with no arguments, it should produce an empty list.
    if not args:
        return None

    List = args[0] 

    if List == None:
        return concat(args[1:])
    
    # Calling concat on any elements that are not lists should result in a SnekEvaluationError
    if not is_type_pair(List): 
        raise SnekEvaluationError("can only concat List objects")

    # make new copy 
    new = Pair(List.car, None)
    cur = new
    while List.cdr != None:
        List = List.cdr
        if List != None and not is_type_pair(List):
            raise SnekEvaluationError("None list element")
        cur.cdr = Pair(List.car, None)
        cur = cur.cdr
    
    # recursive step 
    cur.cdr = concat(args[1:])

    return new


def _map(args):
    """ 
    (map FUNCTION LIST) takes a function and a list as arguments,
    returns a new list containing the results of applying the given function to each element of the given list. 
    (map (function (x) (* 2 x)) (list 1 2 3)) -> the list (2 4 6).
    """
    func, List = args[0], args[1]

    if List == None:
        return None

    if not is_type_pair(List): raise SnekEvaluationError("not a Pair object")

    new = Pair(func([List.car]), None)
    cur = new
    while List.cdr != None:
        List = List.cdr
        if List != None and not is_type_pair(List):
            raise SnekEvaluationError("Not a Pair object")
        cur.cdr = Pair(func([List.car]), None)
        cur = cur.cdr

    return new  


def _filter(args):
    """ 
    (filter FUNCTION LIST) takes a function and a list as arguments, 
    returns a new list containing only the elements of the given list for which the given function returns true.
    (filter (function (x) (> x 0)) (list -1 2 -3 4)) -> the list (2 4).
    """
    func, List = args[0], args[1]

    if List == None:
        return None

    if not is_type_pair(List): raise SnekEvaluationError

    if func([List.car]):
        new = Pair(List.car, _filter([func, List.cdr]))
    else:
        new = _filter([func, List.cdr])

    return new  



def _reduce(args):
    """
    (reduce FUNCTION LIST INITVAL) takes a function, a list, and an initial value as inputs. 
    It produces its output by successively applying the given function to the elements in the list, 
    maintaining an intermediate result along the way.
    """
    func, List, initial = args[0], args[1], args[2]

    if List == None:
        return initial
    if not is_type_pair(List): raise SnekEvaluationError

    new_intial = func([initial, List.car])
    next_list = List.cdr

    return _reduce([func, next_list, new_intial])
    
def begin(args, environment):
    """
    return its last argument
    all of the arguments are evaluated in turn
    (begin (:= x 7) (:= y 8) (- x y)) -> -1
    (begin (:= y 2) (:= (square x) (* x x)) (square 2)) -> 4 
    """
    for i in range(len(args)-1):
        evaluate(args[i], environment)
    
    return evaluate(args[-1], environment)



def delete(args, environment):
    """
    del is used for deleting variable bindings within the current environment.
    (del VAR)
    If the given variable is bound in the current environment, its binding should be removed and the associated value should be returned. 
    If VAR is not bound locally, this special form should raise a SnekNameError.
    """
    var = args[0]
    if var in environment:
        val = environment[var]
        del environment[var]
        return val 
    else:
        raise SnekNameError(f"{var} is not bound in the local frame")
    


def let(args, environment):
    """
    let is used for creating local variable definitions. 
    It takes the form: (let ((VAR1 VAL1) (VAR2 VAL2) (VAR3 VAL3) ...) BODY)
    Evaluating all the given values in the current environment.
    Creating a new environment whose parent is the current environment, binding each name to its associated value in this new environment.
    Evaluating the BODY expression in this new environment (this value is the result of evaluating the let special form).
    Note: the given bindings are only available in the body of the let expression
    """
    # new environment 
    new = Environment()
    new.parent = environment

    var_val, body = args
    
    for pair in var_val:
        var = pair[0]
        val = evaluate(pair[1], environment)
        new[var] = val
        
    return evaluate(body, new)



def set_bang(args, environment):
    """
    set! is used for changing the value of an existing variable
    It takes the form: (set! VAR EXPR)
    Evaluating the given expression in the current environment
    Finding the nearest enclosing environment in which VAR is defined (starting from the current environment and working upward until it finds a binding), and updating its binding in that environment to be the result of evaluating EXPR 
    If VAR is not defined in any environments in the chain, set! should raise a SnekNameError.
    """
    var, exp = args[0], evaluate(args[1], environment)

    cur = environment 
    while var not in cur.variables:
        if isinstance(cur.parent, Environment):
            cur = cur.parent
        else: 
            raise SnekNameError(f"didn't find {var}")

    # cur is the correct environment
    cur[var] = exp
    return exp 


snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': mul,
    '/': div,
    '#t': True, 
    '#f': False, 
    '=?': equal,
    '>': decrease,
    '>=': nonincrease,
    '<': increase,
    '<=': nondecrease,
    'and': _and,
    'or': _or,
    'not': _not,
    'car': car, 
    'cdr': cdr, 
    'nil': None,
    'list': linked_list,
    'length': length,
    'elt-at-index': elt_at_index, 
    'concat': concat,
    'map': _map,
    'filter': _filter,
    'reduce': _reduce,
}


##############
# Evaluation #
##############


class Environment:
    def __init__(self):
        self.parent = None
        self.variables = dict()
    
    def __getitem__(self, symbol):
        if symbol in self.variables:
            return self.variables[symbol]
        else:
            if self.parent is not None:
                return self.parent[symbol]
            else:
                raise SnekNameError(f"didn't find {symbol} in {self.parent}")

    def __setitem__(self, symbol, exp):
        self.variables[symbol] = exp 


    def __contains__(self, key):
        if type(key) != str:
            return False
        elif key in self.variables:
            return True
        elif self.parent:
            return key in self.parent
        else:
            return False

    def __delitem__(self, key):
        if key in self.variables:
            del self.variables[key]
        else:
            raise SnekNameError(f"didn't find {key} in {self.variables}")




keywords = {':=', 'function', 'if', 'and', 'or', 'cons', 'begin', 'del', 'let', 'set!'}

def evaluate(tree, environment=None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    >>> evaluate(3.14)
    3.14
    >>> evaluate(['+', 3, 7, 2])
    12
    >>> evaluate(['+', 3, ['-', 7, 5]])
    5
    """

    if environment == None:
        # If no environment is passed in, an empty environment should be used
        # parent is an environment containing all the bindings from the snek_builtins dictionary.
        environment = Environment()
        environment.parent = builtin


    # Base Case: If the expression is a number, return that number.
    if type(tree) == int or type(tree) == float:
        return tree

    # Base Case: If the expression is a variable/string/function, return its value 
    if tree in environment:
        return environment[tree]
    
    if type(tree) != list:
        raise SnekNameError(f"didn't find {tree} in {environment.variables}")

    # print(tree)
    if tree == []:
        raise SnekEvaluationError("empty expression")

    first, rest = tree[0], tree[1:] 

    if first in environment and first not in keywords:
        # if is a variable 
        first = environment[first]

    elif not isinstance(first, str) or first not in keywords:
        # if is an expression (not a keyword)
        first = evaluate(first, environment)


    if first == 'function':
        return Function(rest[0], rest[1], environment) # create a new Function object 
    
    elif first == ':=':
        second = rest[0]
        third = rest[1]
        if isinstance(second, str): # e.g. (:= square (function (x) (* x x)))
            expr = evaluate(third, environment)
            environment[second] = expr
            return expr
    
        if isinstance(second, list): # e.g. (:= (add2 x y) (+ x y))
            name = second[0]
            parameters = second[1:]
            func = Function(parameters, third, environment)
            environment[name] = func
            return func

    # modify your evaluate function so that it properly handles the if special form
    elif first == 'if':
        cond = rest[0]
        if evaluate(cond, environment):
            return evaluate(rest[1], environment)
        return evaluate(rest[2], environment)

    elif first == 'and' or first == 'or':
        logical_op = environment[first] # _and() or _or()
        return logical_op(rest, environment) # do not evaluate here, pass it to the function

    elif first == 'cons':
        return cons(rest, environment)

    elif first == 'begin':
        return begin(rest, environment)
    
    elif first == 'del':
        return delete(rest, environment)

    elif first == 'let':
        return let(rest, environment)
    
    elif first == 'set!':
    
        return set_bang(rest, environment)

    else:
        # is a function call e.g. (square 2)
        params = []
        for i in rest:
            params.append(evaluate(i, environment))
        
        # should be a callable function 
        # print('first is', first, 'params', params)
        if callable(first):
            return first(params) 
        else:
            raise SnekEvaluationError("invalid function")



def result_and_env(tree, environment=None):
    """
    returns a tuple with two elements: 
        * the result of the evaluation 
        * the environment in which the expression was evaluated
    """
    # If no envxironment is given, make a brand new environment. 
    if environment == None:
        environment = Environment()
        environment.parent = builtin

    # evaluat the expression in that environment 
    result = evaluate(tree, environment)

    return (result, environment)


class Function:
    # the code representing the body of the function (which, for now, is restricted to a single expression representing the return value)
    # the names of the function's parameters
    # a pointer to the environment in which the function was defined
    def __init__(self, parameters, body, define_env):
        self.parameters = parameters
        self.body = body
        self.define_env = define_env 

    def __call__(self, args):
        # make a new environment whose parent is the define environment 
        new_env = Environment()
        new_env.parent = self.define_env

        if len(self.parameters) != len(args):
            # arguments mismatch 
            raise SnekEvaluationError("incorrect number of arguments")

        # in the new environment, bind the function's parameters to the arguments that are passed to it
        for p, arg in zip(self.parameters, args):
            new_env[p] = arg

        # evaluate the body of the function in that new environment.
        result = evaluate(self.body, new_env)
        
        return result 
    
    def __str__(self):
        return f"new Function Object with params ({self.parameters}) and body ({self.body})"

class Pair:
    """ represent a cons cell """
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return f"({self.car}), ({self.cdr})"


builtin = Environment()
builtin.variables = snek_builtins

def REPL(environment=None):
    """
    accepts input from the user, tokenizes and parses it, 
    evaluates it, and prints sthe result.
    """
    if not environment:
        environment = Environment()
        environment.parent = builtin

    while True:
        print("in> ", end='')
        inp = input()
        if inp == 'QUIT' or inp == "q": break
        tokens = tokenize(inp)
        try:
            parsed_exp = parse(tokens)
        except SnekSyntaxError as error:
            print(error)
            continue
        try:
            result = evaluate(parsed_exp, environment)
        except SnekNameError as error:
            print(error)
            continue  
        except SnekEvaluationError as error:
            print(error)
            continue
        
        print("out>", result)


def evaluate_file(filename, environment=None):
    """ return the result of evaluating the expression contained in the file """
    file = open(filename)
    source = file.read()
    file.close()

    if not environment:
        environment = Environment()
        environment.parent = builtin

    tokens = tokenize(source)
    parsed = parse(tokens)
    result = evaluate(parsed, environment)

    return result 



if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    # import definitions 
    environment = Environment()
    environment.parent = builtin
    for file in sys.argv[1:]:
        evaluate_file(file, environment)
    REPL(environment)

