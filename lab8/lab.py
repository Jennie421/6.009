import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __add__(self, other):
        return Add(self, other)
    def __radd__(self, other):
        return Add(other, self)
    
    def __sub__(self, other):
            return Sub(self, other)
    def __rsub__(self, other):
        return Sub(other, self)
    
    def __mul__(self, other):
        return Mul(self, other)
    def __rmul__(self, other):
        return Mul(other, self)
    
    def __truediv__(self, other):
        return Div(self, other)
    def __rtruediv__(self, other):
        return Div(other, self)


class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    precedence = 3
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'
    
    def deriv(self, sym):
        if str(self) == sym:
            return 1
        else:
            return 0

    def simplify(self):
        return self

    def eval(self, mapping):
        if self.name not in mapping:
            raise Exception ("No value for variable {self.name}")
        return mapping[self.name]



class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    precedence = 3

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'
    
    def deriv(self, sym):
        return Num(0)

    def simplify(self):
        return self 

    def eval(self, mapping):
        return self.n



class BinOp(Symbol):
    def __init__(self, left, right):
        if isinstance(left, int) or isinstance(left, float):
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            assert isinstance(left, Symbol) # e.g. Add(...)
            self.left = left 

        if isinstance(right, int) or isinstance(right, float):
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            assert isinstance(right, Symbol) 
            self.right = right 

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"
    
    def __str__(self):
        if self.left.precedence < self.precedence:
            left_str = f"({self.left})"
        else:
            left_str = str(self.left)

        if self.right.precedence < self.precedence:
            right_str = f"({self.right})"
        elif self.parenthesization and self.right.precedence == self.precedence:
            right_str = f"({self.right})"
        else:
            right_str = str(self.right)

        return f"{left_str} {self.op} {right_str}"
    
    def simplify():
        pass        


def is_zero(E):
    if E.__class__.__name__ == "Num": 
        if E.n == 0:
            return True 
    return False

def is_one(E):
    if E.__class__.__name__ == "Num": 
        if E.n == 1:
            return True 
    return False


class Add(BinOp):
    op = '+'
    precedence = 1
    parenthesization = False 
    
    def deriv(self, sym):
        return self.left.deriv(sym) + self.right.deriv(sym)
    

    def simplify(self):
        simple_left = self.left.simplify()
        simple_right = self.right.simplify()

        if simple_left.__class__.__name__ == "Num" and simple_right.__class__.__name__ == "Num":
            return Num(simple_left.n + simple_right.n)

        # E + 0 or 0 + E = 0 
        if is_zero(simple_left):
            return simple_right
        elif is_zero(simple_right):
            return simple_left
        else:
            return Add(simple_left, simple_right)
        # BinOp.simplify()
        
    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return left + right


class Sub(BinOp):
    op = '-'
    precedence = 1
    parenthesization = True
    
    def deriv(self, sym):
        return self.left.deriv(sym) - self.right.deriv(sym)

    def simplify(self):
        simple_left = self.left.simplify()
        simple_right = self.right.simplify()

        if simple_left.__class__.__name__ == "Num" and simple_right.__class__.__name__ == "Num":
            return Num(simple_left.n - simple_right.n)

        # E - 0 = 0 
        if is_zero(simple_right):
            return simple_left
        else:
            return Sub(simple_left, simple_right)

    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return left - right


class Mul(BinOp):
    op = '*'
    precedence = 2
    parenthesization = False

    def deriv(self, sym):
        return self.left * self.right.deriv(sym) + self.right * self.left.deriv(sym)

    def simplify(self):
        simple_left = self.left.simplify()
        simple_right = self.right.simplify()

        if simple_left.__class__.__name__ == "Num" and simple_right.__class__.__name__ == "Num":
            return Num(simple_left.n * simple_right.n) 
        
        # E * 0 = 0 
        if is_zero(simple_left) or is_zero(simple_right):
            return Num(0)
        # E * 1 or 1 * E = 0 
        elif is_one(simple_left):
            return simple_right
        elif is_one(simple_right):
            return simple_left
        else:
            return Mul(simple_left, simple_right)

    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return left * right



class Div(BinOp):
    op = '/'
    precedence = 2
    parenthesization = True
    
    def deriv(self, sym):
        u = self.left
        v = self.right
        du = self.left.deriv(sym)
        dv = self.right.deriv(sym)
        return (v * du - u * dv)/(v*v)

    def simplify(self):
        simple_left = self.left.simplify()
        simple_right = self.right.simplify()

        if simple_left.__class__.__name__ == "Num" and simple_right.__class__.__name__ == "Num":
            return Num(simple_left.n / simple_right.n) 
        
        # E / 0 = 0 
        if is_zero(simple_right):
            return Num(0)
        # E / 1 = E
        elif is_one(simple_right):
            return simple_left
        else:
            return Div(simple_left, simple_right)

    def eval(self, mapping):
        left = self.left.eval(mapping)
        right = self.right.eval(mapping)
        return left / right



digits = [ str(n) for n in range(0, 10)]

def is_digit(x):
    if x in digits:
        return True
    return False

def tokenize(s):
    """
    takes a string as input
    returns a list of meaningful tokens (parentheses, variable names, numbers, or operands)
    >>> tokenize("(x * (200 + 3))")
    ['(', 'x', '*', '(', '200', '+', '3', ')', ')']
    """
    output = []
    i = 0 
    while i < len(s):
        if (s[i] == '-' and is_digit(s[i+1])) or (is_digit(s[i]) and is_digit(s[i+1])): 
            # if is a negative number or has >= 2 digits 
            token = s[i] + s[i+1]
            i = i + 2
            while i < len(s) and is_digit(s[i]):
                token += s[i]
                i += 1
            output.append(token)
        
        elif s[i] == ' ':
            i += 1
            continue
        
        else:
            output.append(s[i])
            i += 1
    return output 



def parse(tokens):
    """
    take the output of tokenize and converts it into an appropriate instance of `Symbol` (or some subclass thereof)
    >>> tokens = tokenize("(x * (2 + 3))")
    >>> parse(tokens)
    Mul(Var('x'), Add(Num(2), Num(3)))
    """
    def parse_expression(index):
        try:
            return Num(int(tokens[index])), index+1
        except: 
            pass

        if tokens[index] == '(':
            left_expression, next_index = parse_expression(index+1)
            op = tokens[next_index]
            right_expression, next_index = parse_expression(next_index+1)
            if op == '+':
                return Add(left_expression, right_expression), next_index + 1
            elif op == '-':
                return Sub(left_expression, right_expression), next_index + 1
            elif op == '*':
                return Mul(left_expression, right_expression), next_index + 1
            elif op == '/':
                return Div(left_expression, right_expression), next_index + 1

        else:
            return Var(tokens[index]), index+1


    parsed_expression, next_index = parse_expression(0)
   
    return parsed_expression



def sym(s):
    """
    Parse strings into symbolic expressions 
    The input string should contain either:
        a single variable name,
        a single number, or
        a fully parenthesized expression of the form (E1 op E2), representing a binary operation 
    >>> sym('(x * (2 + 3))')
    Mul(Var('x'), Add(Num(2), Num(3)))
    """
    tokens = tokenize(s)
    exp = parse(tokens)
    return exp 


if __name__ == '__main__':
    doctest.testmod()
    x = Var('x')
    y = Var('y')
    z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
    
    print(tokenize("(x * (200 + 3))"))
    print(tokenize('20'))
