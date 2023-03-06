#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!


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
            raise SnekSyntaxError
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
    if tokens[0] != '(': raise SnekSyntaxError

    layers = [[]]

    for i, token in enumerate(tokens): # e.g. ((:= x 3)
        if token == '(':
            layers.append([]) 
        elif token == ')':
            cur_layer = layers.pop()
            if not layers:
                # if parentheses are mismatched in the input, extra ")"
                raise SnekSyntaxError
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
        raise SnekSyntaxError 
    
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
            if len(parsed) != 3: raise SnekSyntaxError
            # if the second element in a := statement is neither a name nor a list containing one or more parameters (strings representing paramater names).
            if not isinstance(parsed[1], str) and not isinstance(parsed[1], list): raise SnekSyntaxError
            if not parsed[1]: raise SnekSyntaxError
            # all in second element must be string
            if not all([type(i) == str for i in parsed[1]]): raise SnekSyntaxError
            check_syntax(parsed[2])
        elif first == 'function':
            if len(parsed) != 3: raise SnekSyntaxError
            if not isinstance(parsed[1], list): raise SnekSyntaxError
            if not all([isinstance(i, str) for i in parsed[1]]): raise SnekSyntaxError # separate helper func
            check_syntax(parsed[2])

    check_syntax(parsed)

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

snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': mul,
    "/": div,
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
                raise SnekNameError

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
        raise SnekNameError

    first, rest = tree[0], tree[1:] 

    if first in environment:
        # if is a variable 
        first = environment[first]

    elif first != ':=' and first != 'function':
        # if is an expression (not a keyword)
        first = evaluate(first, environment)

    # if it is a list whose first element is not a valid function, it should raise a SnekEvaluationError5
    # if type(first) == int or type(first) == float:
    #     raise SnekEvaluationError

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

    else:
        # is a function call e.g. (square 2)
        output = []
        for i in rest:
            output.append(evaluate(i, environment))

        if callable(first):
            return first(output) 
        else:
            raise SnekEvaluationError




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
            raise SnekEvaluationError

        # in the new environment, bind the function's parameters to the arguments that are passed to it
        for p, arg in zip(self.parameters, args):
            new_env[p] = arg

        # evaluate the body of the function in that new environment.
        result = evaluate(self.body, new_env)
        
        return result 
    



builtin = Environment()
builtin.variables = snek_builtins

def REPL():
    """
    accepts input from the user, tokenizes and parses it, 
    evaluates it, and prints sthe result.
    """
    environment = Environment()
    environment.parent = builtin
    while True:
        print("in> ", end='')
        inp = input()
        if inp == 'QUIT' or inp == "q": break
        tokens = tokenize(inp)
        try:
            parsed_exp = parse(tokens)
        except SnekSyntaxError:
            print('syntax Error: Parentheses are mismatched')
            continue
        try:
            result = evaluate(parsed_exp, environment)
        except SnekNameError:
            print('Name Error: Expression is a symbol that is not defined')
            continue  
        except SnekEvaluationError:
            print('Evaluation error: Not a valid function')
            continue
        
        print("out>", result)




if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    # (:= x 5)
    # (:= x2 (* x x))
    # (+ x2 x)
    REPL()


    # print(parse(['(', ':=', '(', ')', 'x', ')']))
