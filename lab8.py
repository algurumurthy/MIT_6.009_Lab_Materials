#import doctest
#
## NO ADDITIONAL IMPORTS ALLOWED!
## You are welcome to modify the classes below, as well as to implement new
## classes and helper functions as necessary.
#
#def tokenize(text):
#    """
#    Should take a string, or text, as described above as input and should 
#    output a list of meaningful tokens (parentheses, variable names, numbers, 
#    or operands)
#    """
#    digits = '0123456789'
#    final_list = []
#    for index in range(len(text)):
#        final_index = len(final_list) - 1
#        indext = len(text[index-1]) - 1
#        try:
#            if text[index-1][indext] in digits: 
#                if text[index] in digits:
#                    final_list[final_index] += text[index]
#                    continue
#            elif (final_list[final_index] == "-" and text[index-1] != " "):
#                if text[index] in digits:
#                    final_list[final_index] += text[index]
#                    continue
#        except:
#            pass
#        if text[index] == ' ':
#            continue
#        final_list.append(text[index])
#    final_tuple = tuple(final_list)
#    return final_tuple
#
#
#def parse_expression(tokens, index):
#    """
#    Recursive function that takes as an argument an integer into the tokens 
#    list and returns a pair of values. The first is an expression found 
#    starting at the location given by index (an instance of one of the Symbol 
#    subclasses). The second is the index beyond where this expression ends.
#    """
#    alphabets = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#    current_token = tokens[index]
#    if current_token == '(':
#        parsed_left = parse_expression(tokens, index+1)[0]
#        left_index = parse_expression(tokens, index+1)[1]
#        parsed_right = parse_expression(tokens, left_index+1)[0]
#        right_index = parse_expression(tokens, left_index+1)[1]
#        if tokens[left_index] == '-':
#            return (Sub(parsed_left, parsed_right), right_index + 1)
#        if tokens[left_index] == '+':
#            return (Add(parsed_left, parsed_right), right_index + 1)
#        if tokens[left_index] == '*':
#            return (Mul(parsed_left, parsed_right), right_index + 1)
#        if tokens[left_index] == '/':
#            return (Div(parsed_left, parsed_right), right_index + 1)
#    if current_token in alphabets:
#        return (Var(current_token), index + 1)
#    return (Num(int(current_token)), index+1)
#
#
#def parse(tokens):
#    """
#    Takes the output of tokenize and convert it into an appropriate instance of 
#    Symbol (or some subclass thereof).
#    """
#    return parse_expression(tokens, 0)[0]
#
#
#def sym(data):
#    """
#    Given a certain input of data, mainly a string, it returns a parsed and 
#    valid symbol object which is then returned.
#    """
#    symbol_object = parse(tokenize(data))
#    return symbol_object
#
#
#class Symbol:
#    """
#    Our base class; all other classes we create will inherit from this class, 
#    and any behavior that is common between all expressions (that is, all 
#    behavior that is not unique to a particular kind of symbolic expression)
#    """
#    def __add__(self, other):
#        """
#        Represents the addition of two expressions in its left-to-right format
#        """
#        return Add(self, other)
#
#    def __mul__(self, other):
#        """
#        Represents the multiplication of two expressions in its left-to-right 
#        format
#        """
#        return Mul(self, other)
#
#    def __truediv__(self, other):
#        """
#        Represents the division of two expressions in its left-to-right format
#        """
#        return Div(self, other)
#
#    def __sub__(self, other):
#        """
#        Represents the subtraction of two expressions in its left-to-right 
#        format
#        """
#        return Sub(self, other)
#
#    def __radd__(self, other):
#        """
#        Represents the addition of two expressions in the reverse format
#        """
#        return Add(other, self)
#
#    def __rmul__(self, other):
#        """
#        Represents the multiplication of two expressions in the reverse format
#        """
#        return Mul(other, self)
#
#    def __rtruediv__(self, other):
#        """
#        Represents the division of two expressions in the reverse format
#        """
#        return Div(other, self)
#
#    def __rsub__(self, other):
#        """
#        Represents the subtraction of two expressions in the reverse format
#        """
#        return Sub(other, self)
#
#
#class Num(Symbol):
#    """
#    The class that deals with the representations and operations with numbers,
#    and has no associated symbols
#    """
#    sym = None
#
#    def __init__(self, n):
#        """
#        Initializer.  Store an instance variable called `n`, containing the
#        value passed in to the initializer.
#        """
#        self.n = n
#
#    def __str__(self):
#        """
#        Returns the string representatino of what the number is supposed to 
#        like, in this case, the value
#        """
#        return str(self.n)
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        return 'Num(' + repr(self.n) + ')'
#
#    def deriv(self, level):
#        """
#        Returns the base case of how a number is to be derived given a 
#        certain level of derivation having been completed, which is always
#        generally zero
#        """
#        return Num(0)
#
#    def simplify(self):  # base case
#        """
#        Again another base case method that just returns the number because
#        there is no other way to simplify it
#        """
#        return self
#
#    def eval(self, mapping):
#        """
#        Since there is no other way to evaluate what a number amounts to, in 
#        order to evaluate it we can just return its value, or in this case, 
#        self.n
#        """
#        return self.n
#
#
#class Var(Symbol):
#    """
#    Sub-Class of Symbol to represent a single variable and methods to define a
#    series of base cases for other operations and has no associated symbols.
#    """
#    sym = None
#
#    def __init__(self, n):
#        """
#        Initializer.  Store an instance variable called `name`, containing the
#        value passed in to the initializer.
#        """
#        self.name = n
#
#    def __str__(self):
#        """
#        Returns the string representatino of what the variable is supposed to 
#        like, in this case, the name
#        """
#        return self.name
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        return 'Var(' + repr(self.name) + ')'
#
#    def deriv(self, level):
#        """
#        Returns the base case of how a variable is to be derived given a 
#        certain level of derivation having been completed
#        """
#        if self.name == level:
#            return Num(1)
#        return Num(0)
#
#    def simplify(self):  # base case
#        """
#        Again another base case method that just returns the variable because
#        there is no other way to simplify it
#        """
#        return self
#
#    def eval(self, mapping):
#        """
#        Returns a specific instance of the variable name in the mapping, again 
#        as another base case in the method having gotten down to a single 
#        variable
#        """
#        final_eval = mapping[self.name]
#        return final_eval
#
#
#class BinOp(Symbol):
#    """
#    Represents a binary operation. Because it is a type of symbolic expression, 
#    BinOp should be a subclass of Symbol, and it shows how to combine two items
#    """
#    def __init__(self, left, right):
#        """
#        Initializer.  Store an instance variable called `left` and 'right', 
#        containing the left and right peices of a certain expression and 
#        determines whether or not the object is to be classified as a "num"
#        or a "var"
#        """
#        if isinstance(right, Symbol):
#            self.right = right
#        else:
#            if isinstance(right, str):
#                self.right = Var(right)
#            else:
#                self.right = Num(right)
#        if isinstance(left, Symbol):
#            self.left = left
#        else:
#            if isinstance(left, str):
#                self.left = Var(left)
#            else:
#                self.left = Num(left)
#                
#    def deriv(self, sym, level):
#        """
#        This method should take a single argument (a string containing the name 
#        of the variable with respect to which we are differentiating), and it 
#        should return a symbolic expression representing the result of the 
#        differentiation given a level of differentiation
#        """
#        if sym == '+':
#            right_deriv = self.right.deriv(sym, level)
#            left_deriv = self.left.deriv(sym, level)
#            exp = left_deriv + right_deriv
#            return exp
#        elif sym == '-':
#            right_deriv = self.right.deriv(sym, level)
#            left_deriv = self.left.deriv(sym, level)
#            exp = left_deriv - right_deriv
#            return exp
#        elif sym == '*':
#            return self.left * self.right.deriv(sym, level) + self.right * self.left.deriv(sym, level)
#        elif sym == '/':
#            quotient_denom = (self.right * self.right)
#            quotient_num = (self.right * self.left.deriv(sym, level)) - (self.left * self.right.deriv(sym, level))
#            return quotient_num / quotient_denom
#        
#    def simplify(self, sym):
#        """
#        Simplify should take no arguments, and it should return a simplified 
#        form of the expression that also follows all mathematical rules such as 
#        order of operations, etc.
#        """
#        right = self.right.simplify(sym)
#        left = self.left.simplify(sym)
#        if sym == '+':
#            if type(right) == Num and type(left) == Num:
#                return Num(left.n + right.n)
#            elif type(right) == Num and right.n == 0:
#                return left
#            elif type(left) == Num and left.n == 0:
#                return right
#            else:
#                return left + right
#        elif sym == '-':
#            if type(right) == Num and type(left) == Num:
#                return Num(left.n - right.n)
#            elif type(right) == Num and right.n == 0:
#                return left
#            else:
#                return left - right
#        elif sym == '*':
#            if type(left) == Num and type(right) == Num:
#                return Num(left.n * right.n)
#            if type(left) == Num and left.n == 0:
#                return Num(0)
#            if type(right) == Num and right.n == 0:
#                return Num(0)
#            if type(left) == Num and left.n == 1:
#                return right
#            if type(right) == Num and right.n == 1:
#                return left
#            return left * right
#        elif sym == '/':
#            if type(right) == Num and type(left) == Num:
#                return Num(left.n / right.n)
#            elif type(left) == Num and left.n == 0:
#                return Num(0)
#            elif type(right) == Num and right.n == 1:
#                return left
#            else:
#                return left / right
#                     
#    def eval(self, sym, mapping):
#        """
#        Evaluates expressions for particular values of variables where mapping 
#        is a dictionary mapping variable names to values
#        """
#        left_map = self.left.eval(sym, mapping)
#        right_map = self.right.eval(sym, mapping)
#        if sym == '+':
#            return left_map + right_map
#        elif sym == '-':
#            return left_map - right_map
#        elif sym == '*':
#            return left_map * right_map
#        elif sym == '/':
#            return left_map / right_map
#
#
#class Add(BinOp):
#    """
#    A subclass to represent Addition with both a symbol to represent how
#    it is mathematically shown and a value to determined its precedence in 
#    the PEMDAS rules of order of operations.
#    """
#    sym = '+'
#    preced = 0
#
#    def __init__(self, left, right):
#        """
#        Initializer.  Store an instance variable called `left` and 'right', 
#        containing the left and right peices of a certain expression. Inherits
#        these from the super() class of BinOp
#        """
#        super().__init__(left, right)
#
#    def __str__(self):
#        """
#        Accounts for the representation of the class's operation, including 
#        how it needs to be represented with certain parenthesization 
#        requirements
#        """
#        sym = ' ' + self.sym + ' '
#        left_side = str(self.left)
#        right_side = str(self.right)
#        exp = left_side + sym + right_side
#        return exp
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        exp = "Add(" + repr(self.left) + ", " + repr(self.right) + ")"
#        return exp
#
#    def simplify(self):
#        """
#        Simplify should take no arguments, and it should return a simplified 
#        form of the expression that also follows all mathematical rules such as 
#        order of operations, etc.
#        """
##        right = self.right.simplify()
##        left = self.left.simplify()
##        if type(right) == Num and type(left) == Num:
##            return Num(left.n + right.n)
##        elif type(right) == Num and right.n == 0:
##            return left
##        elif type(left) == Num and left.n == 0:
##            return right
##        else:
##            return left + right
#        return super().simplify(sym)
#
#    def deriv(self, level):
#        """
#        This method should take a single argument (a string containing the name 
#        of the variable with respect to which we are differentiating), and it 
#        should return a symbolic expression representing the result of the 
#        differentiation given a level of differentiation
#        """
##        right_deriv = self.right.deriv(level)
##        left_deriv = self.left.deriv(level)
##        exp = left_deriv + right_deriv
##        return exp
#        return super().deriv(sym, level)
#
#    def eval(self, mapping):
#        """
#        Evaluates expressions for particular values of variables where mapping 
#        is a dictionary mapping variable names to values
#        """
##        left_map = self.left.eval(mapping)
##        right_map = self.right.eval(mapping)
##        return left_map + right_map
#        return super().eval(sym, mapping)
#
#
#class Sub(BinOp):
#    """
#    A subclass to represent Subtraction with both a symbol to represent how
#    it is mathematically shown and a value to determined its precedence in 
#    the PEMDAS rules of order of operations.
#    """
#    sym = "-"
#    preced = 0
#
#    def __init__(self, left, right):
#        """
#        Initializer.  Store an instance variable called `left` and 'right', 
#        containing the left and right peices of a certain expression. Inherits
#        these from the super() class of BinOp
#        """
#        super().__init__(left, right)
#
#    def __str__(self):
#        """
#        Accounts for the representation of the class's operation, including 
#        how it needs to be represented with certain parenthesization 
#        requirements
#        """
#        left_part = str(self.left)
#        right_part = str(self.right)
#        if self.right.sym is not None:
#            if self.right.preced == 0:
#                right_part = '(' + right_part + ')'
#        sym = ' ' + self.sym + ' '
#        exp = left_part + sym + right_part
#        return exp
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        exp = "Sub(" + repr(self.left) + ", " + repr(self.right) + ")"
#        return exp
#
#    def simplify(self):
#        """
#        Simplify should take no arguments, and it should return a simplified 
#        form of the expression that also follows all mathematical rules such as 
#        order of operations, etc.
#        """
##        right = self.right.simplify()
##        left = self.left.simplify()
##        if type(right) == Num and type(left) == Num:
##            return Num(left.n - right.n)
##        elif type(right) == Num and right.n == 0:
##            return left
##        else:
##            return left - right
#        return super().simplify(sym)
#
#    def deriv(self, level):
#        """
#        This method should take a single argument (a string containing the name 
#        of the variable with respect to which we are differentiating), and it 
#        should return a symbolic expression representing the result of the 
#        differentiation given a level of differentiation
#        """
##        right_deriv = self.right.deriv(level)
##        left_deriv = self.left.deriv(level)
##        exp = left_deriv - right_deriv
##        return exp
#        return super().deriv(sym, level)
#
#    def eval(self, mapping):
#        """
#        Evaluates expressions for particular values of variables where mapping 
#        is a dictionary mapping variable names to values
#        """
##        left_map = self.left.eval(mapping)
##        right_map = self.right.eval(mapping)
##        return left_map - right_map
#        return super().eval(sym, mapping)
#
#
#class Div(BinOp):
#    """
#    A subclass to represent Division with both a symbol to represent how
#    it is mathematically shown and a value to determined its precedence in 
#    the PEMDAS rules of order of operations.
#    """
#    sym = '/'
#    preced = 1
#
#    def __init__(self, left, right):
#        """
#        Initializer.  Store an instance variable called `left` and 'right', 
#        containing the left and right peices of a certain expression. Inherits
#        these from the super() class of BinOp
#        """
#        super().__init__(left, right)
#
#    def __str__(self):
#        """
#        Accounts for the representation of the class's operation, including 
#        how it needs to be represented with certain parenthesization 
#        requirements
#        """
#        left_part = str(self.left)
#        right_part = str(self.right)
#        if self.left.sym is not None:
#            if self.left.preced == 0:
#                left_part = '(' + left_part + ')'
#        if self.right.sym is not None:
#            if self.right.preced == 0:
#                right_part = '(' + right_part + ')'
#            elif self.right.preced == 1:
#                right_part = '(' + right_part + ')'
#        sym = ' ' + self.sym + ' '
#        exp = left_part + sym + right_part
#        return exp
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        exp = "Div(" + repr(self.left) + ", " + repr(self.right) + ")"
#        return exp
#
#    def simplify(self):
#        """
#        Simplify should take no arguments, and it should return a simplified 
#        form of the expression that also follows all mathematical rules such as 
#        order of operations, etc.
#        """
##        right = self.right.simplify()
##        left = self.left.simplify()
##        if type(right) == Num and type(left) == Num:
##            return Num(left.n / right.n)
##        elif type(left) == Num and left.n == 0:
##            return Num(0)
##        elif type(right) == Num and right.n == 1:
##            return left
##        else:
##            return left / right
#        return super().simplify(sym)
#
#    def deriv(self, level):
#        """
#        This method should take a single argument (a string containing the name 
#        of the variable with respect to which we are differentiating), and it 
#        should return a symbolic expression representing the result of the 
#        differentiation given a level of differentiation
#        """
##        quotient_denom = (self.right * self.right)
##        quotient_num = (self.right * self.left.deriv(level)) - (self.left * self.right.deriv(level))
##        return quotient_num / quotient_denom
#        return super().deriv(sym, level)
#
#    def eval(self, mapping):
#        """
#        Evaluates expressions for particular values of variables where mapping 
#        is a dictionary mapping variable names to values
#        """
##        return self.left.eval(mapping) / self.right.eval(mapping)
#        return super().eval(sym, mapping)
#
#
#class Mul(BinOp):
#    """
#    A subclass to represent Multiplication with both a symbol to represent how
#    it is mathematically shown and a value to determined its precedence in 
#    the PEMDAS rules of order of operations.
#    """
#    sym = '*'
#    preced = 1
#
#    def __init__(self, left, right):
#        """
#        Initializer.  Store an instance variable called `left` and 'right', 
#        containing the left and right peices of a certain expression. Inherits
#        these from the super() class of BinOp
#        """
#        super().__init__(left, right)
#
#    def __str__(self):
#        """
#        Accounts for the representation of the class's operation, including 
#        how it needs to be represented with certain parenthesization 
#        requirements
#        """
#        left_part = str(self.left)
#        right_part = str(self.right)
#        if self.left.sym is not None:
#            if self.left.preced == 0:
#                left_part = '(' + left_part + ')'
#        if self.right.sym is not None:
#            if self.right.preced == 0:
#                right_part = '(' + right_part + ')'
#        sym = ' ' + self.sym + ' '
#        exp = left_part + sym + right_part
#        return exp
#
#    def __repr__(self):
#        """
#        Produces something that can actually be fed back into python but 
#        essentially represents the way in which one should call the method
#        in a different context/a way to represent the function in a Python-
#        friendly way
#        """
#        exp = "Mul(" + repr(self.left) + ", " + repr(self.right) + ")"
#        return exp
#
#    def simplify(self):
#        """
#        Simplify should take no arguments, and it should return a simplified 
#        form of the expression that also follows all mathematical rules such as 
#        order of operations, etc.
#        """
##        right = self.right.simplify()
##        left = self.left.simplify()
##        if type(left) == Num and type(right) == Num:
##            return Num(left.n * right.n)
##        if type(left) == Num and left.n == 0:
##            return Num(0)
##        if type(right) == Num and right.n == 0:
##            return Num(0)
##        if type(left) == Num and left.n == 1:
##            return right
##        if type(right) == Num and right.n == 1:
##            return left
##        return left * right
#        return super().simplify(sym)
#
#    def deriv(self, level):
#        """
#        This method should take a single argument (a string containing the name 
#        of the variable with respect to which we are differentiating), and it 
#        should return a symbolic expression representing the result of the 
#        differentiation given a level of differentiation
#        """
##        return self.left * self.right.deriv(level) + self.right * self.left.deriv(level)
#        return super().deriv(sym, level)
#
#    def eval(self, mapping):
#        """
#        Evaluates expressions for particular values of variables where mapping 
#        is a dictionary mapping variable names to values
#        """
##        return self.left.eval(mapping) * self.right.eval(mapping)
#        return super().eval(sym, mapping)
#
#
#if __name__ == '__main__':
#    x = Div(Add(2, 3), Mul(3, 6))
#    print(repr(x))
#    pass

import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

def tokenize(text):
    """
    Should take a string, or text, as described above as input and should 
    output a list of meaningful tokens (parentheses, variable names, numbers, 
    or operands)
    """
    digits = '0123456789'
    final_list = []
    for index in range(len(text)):
        final_index = len(final_list) - 1
        indext = len(text[index-1]) - 1
        try:
            if text[index-1][indext] in digits: 
                if text[index] in digits:
                    final_list[final_index] += text[index]
                    continue
            elif (final_list[final_index] == "-" and text[index-1] != " "):
                if text[index] in digits:
                    final_list[final_index] += text[index]
                    continue
        except:
            pass
        if text[index] == ' ':
            continue
        final_list.append(text[index])
    final_tuple = tuple(final_list)
    return final_tuple


def parse_expression(tokens, index):
    """
    Recursive function that takes as an argument an integer into the tokens 
    list and returns a pair of values. The first is an expression found 
    starting at the location given by index (an instance of one of the Symbol 
    subclasses). The second is the index beyond where this expression ends.
    """
    alphabets = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    current_token = tokens[index]
    if current_token == '(':
        parsed_left = parse_expression(tokens, index+1)[0]
        left_index = parse_expression(tokens, index+1)[1]
        parsed_right = parse_expression(tokens, left_index+1)[0]
        right_index = parse_expression(tokens, left_index+1)[1]
        if tokens[left_index] == '-':
            return (Sub(parsed_left, parsed_right), right_index + 1)
        if tokens[left_index] == '+':
            return (Add(parsed_left, parsed_right), right_index + 1)
        if tokens[left_index] == '*':
            return (Mul(parsed_left, parsed_right), right_index + 1)
        if tokens[left_index] == '/':
            return (Div(parsed_left, parsed_right), right_index + 1)
    if current_token in alphabets:
        return (Var(current_token), index + 1)
    return (Num(int(current_token)), index+1)


def parse(tokens):
    """
    Takes the output of tokenize and convert it into an appropriate instance of 
    Symbol (or some subclass thereof).
    """
    return parse_expression(tokens, 0)[0]


def sym(data):
    """
    Given a certain input of data, mainly a string, it returns a parsed and 
    valid symbol object which is then returned.
    """
    symbol_object = parse(tokenize(data))
    return symbol_object


class Symbol:
    """
    Our base class; all other classes we create will inherit from this class, 
    and any behavior that is common between all expressions (that is, all 
    behavior that is not unique to a particular kind of symbolic expression)
    """
    def __add__(self, other):
        """
        Represents the addition of two expressions in its left-to-right format
        """
        return Add(self, other)

    def __mul__(self, other):
        """
        Represents the multiplication of two expressions in its left-to-right 
        format
        """
        return Mul(self, other)

    def __truediv__(self, other):
        """
        Represents the division of two expressions in its left-to-right format
        """
        return Div(self, other)

    def __sub__(self, other):
        """
        Represents the subtraction of two expressions in its left-to-right 
        format
        """
        return Sub(self, other)

    def __radd__(self, other):
        """
        Represents the addition of two expressions in the reverse format
        """
        return Add(other, self)

    def __rmul__(self, other):
        """
        Represents the multiplication of two expressions in the reverse format
        """
        return Mul(other, self)

    def __rtruediv__(self, other):
        """
        Represents the division of two expressions in the reverse format
        """
        return Div(other, self)

    def __rsub__(self, other):
        """
        Represents the subtraction of two expressions in the reverse format
        """
        return Sub(other, self)


class Num(Symbol):
    """
    The class that deals with the representations and operations with numbers,
    and has no associated symbols
    """
    sym = None

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        """
        Returns the string representatino of what the number is supposed to 
        like, in this case, the value
        """
        return str(self.n)

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        return 'Num(' + repr(self.n) + ')'

    def deriv(self, level):
        """
        Returns the base case of how a number is to be derived given a 
        certain level of derivation having been completed, which is always
        generally zero
        """
        return Num(0)

    def simplify(self):  # base case
        """
        Again another base case method that just returns the number because
        there is no other way to simplify it
        """
        return self

    def eval(self, mapping):
        """
        Since there is no other way to evaluate what a number amounts to, in 
        order to evaluate it we can just return its value, or in this case, 
        self.n
        """
        return self.n


class Var(Symbol):
    """
    Sub-Class of Symbol to represent a single variable and methods to define a
    series of base cases for other operations and has no associated symbols.
    """
    sym = None

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        """
        Returns the string representatino of what the variable is supposed to 
        like, in this case, the name
        """
        return self.name

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        return 'Var(' + repr(self.name) + ')'

    def deriv(self, level):
        """
        Returns the base case of how a variable is to be derived given a 
        certain level of derivation having been completed
        """
        if self.name == level:
            return Num(1)
        return Num(0)

    def simplify(self):  # base case
        """
        Again another base case method that just returns the variable because
        there is no other way to simplify it
        """
        return self

    def eval(self, mapping):
        """
        Returns a specific instance of the variable name in the mapping, again 
        as another base case in the method having gotten down to a single 
        variable
        """
        final_eval = mapping[self.name]
        return final_eval


class BinOp(Symbol):
    """
    Represents a binary operation. Because it is a type of symbolic expression, 
    BinOp should be a subclass of Symbol, and it shows how to combine two items
    """
    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the left and right peices of a certain expression and 
        determines whether or not the object is to be classified as a "num"
        or a "var"
        """
        if isinstance(right, Symbol):
            self.right = right
        else:
            if isinstance(right, str):
                self.right = Var(right)
            else:
                self.right = Num(right)
        if isinstance(left, Symbol):
            self.left = left
        else:
            if isinstance(left, str):
                self.left = Var(left)
            else:
                self.left = Num(left)


class Add(BinOp):
    """
    A subclass to represent Addition with both a symbol to represent how
    it is mathematically shown and a value to determined its precedence in 
    the PEMDAS rules of order of operations.
    """
    sym = '+'
    preced = 0

    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the left and right peices of a certain expression. Inherits
        these from the super() class of BinOp
        """
        super().__init__(left, right)

    def __str__(self):
        """
        Accounts for the representation of the class's operation, including 
        how it needs to be represented with certain parenthesization 
        requirements
        """
        sym = ' ' + self.sym + ' '
        left_side = str(self.left)
        right_side = str(self.right)
        exp = left_side + sym + right_side
        return exp

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        exp = "Add(" + repr(self.left) + ", " + repr(self.right) + ")"
        return exp

    def simplify(self):
        """
        Simplify should take no arguments, and it should return a simplified 
        form of the expression that also follows all mathematical rules such as 
        order of operations, etc.
        """
        right = self.right.simplify()
        left = self.left.simplify()
        if type(right) == Num and type(left) == Num:
            return Num(left.n + right.n)
        elif type(right) == Num and right.n == 0:
            return left
        elif type(left) == Num and left.n == 0:
            return right
        else:
            return left + right

    def deriv(self, level):
        """
        This method should take a single argument (a string containing the name 
        of the variable with respect to which we are differentiating), and it 
        should return a symbolic expression representing the result of the 
        differentiation given a level of differentiation
        """
        right_deriv = self.right.deriv(level)
        left_deriv = self.left.deriv(level)
        exp = left_deriv + right_deriv
        return exp

    def eval(self, mapping):
        """
        Evaluates expressions for particular values of variables where mapping 
        is a dictionary mapping variable names to values
        """
        left_map = self.left.eval(mapping)
        right_map = self.right.eval(mapping)
        return left_map + right_map


class Sub(BinOp):
    """
    A subclass to represent Subtraction with both a symbol to represent how
    it is mathematically shown and a value to determined its precedence in 
    the PEMDAS rules of order of operations.
    """
    sym = "-"
    preced = 0

    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the left and right peices of a certain expression. Inherits
        these from the super() class of BinOp
        """
        super().__init__(left, right)

    def __str__(self):
        """
        Accounts for the representation of the class's operation, including 
        how it needs to be represented with certain parenthesization 
        requirements
        """
        left_part = str(self.left)
        right_part = str(self.right)
        if self.right.sym is not None:
            if self.right.preced == 0:
                right_part = '(' + right_part + ')'
        sym = ' ' + self.sym + ' '
        exp = left_part + sym + right_part
        return exp

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        exp = "Sub(" + repr(self.left) + ", " + repr(self.right) + ")"
        return exp

    def simplify(self):
        """
        Simplify should take no arguments, and it should return a simplified 
        form of the expression that also follows all mathematical rules such as 
        order of operations, etc.
        """
        right = self.right.simplify()
        left = self.left.simplify()
        if type(right) == Num and type(left) == Num:
            return Num(left.n - right.n)
        elif type(right) == Num and right.n == 0:
            return left
        else:
            return left - right

    def deriv(self, level):
        """
        This method should take a single argument (a string containing the name 
        of the variable with respect to which we are differentiating), and it 
        should return a symbolic expression representing the result of the 
        differentiation given a level of differentiation
        """
        right_deriv = self.right.deriv(level)
        left_deriv = self.left.deriv(level)
        exp = left_deriv - right_deriv
        return exp

    def eval(self, mapping):
        """
        Evaluates expressions for particular values of variables where mapping 
        is a dictionary mapping variable names to values
        """
        left_map = self.left.eval(mapping)
        right_map = self.right.eval(mapping)
        return left_map - right_map


class Div(BinOp):
    """
    A subclass to represent Division with both a symbol to represent how
    it is mathematically shown and a value to determined its precedence in 
    the PEMDAS rules of order of operations.
    """
    sym = '/'
    preced = 1

    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the left and right peices of a certain expression. Inherits
        these from the super() class of BinOp
        """
        super().__init__(left, right)

    def __str__(self):
        """
        Accounts for the representation of the class's operation, including 
        how it needs to be represented with certain parenthesization 
        requirements
        """
        left_part = str(self.left)
        right_part = str(self.right)
        if self.left.sym is not None:
            if self.left.preced == 0:
                left_part = '(' + left_part + ')'
        if self.right.sym is not None:
            if self.right.preced == 0:
                right_part = '(' + right_part + ')'
            elif self.right.preced == 1:
                right_part = '(' + right_part + ')'
        sym = ' ' + self.sym + ' '
        exp = left_part + sym + right_part
        return exp

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        exp = "Div(" + repr(self.left) + ", " + repr(self.right) + ")"
        return exp

    def simplify(self):
        """
        Simplify should take no arguments, and it should return a simplified 
        form of the expression that also follows all mathematical rules such as 
        order of operations, etc.
        """
        right = self.right.simplify()
        left = self.left.simplify()
        if type(right) == Num and type(left) == Num:
            return Num(left.n / right.n)
        elif type(left) == Num and left.n == 0:
            return Num(0)
        elif type(right) == Num and right.n == 1:
            return left
        else:
            return left / right

    def deriv(self, level):
        """
        This method should take a single argument (a string containing the name 
        of the variable with respect to which we are differentiating), and it 
        should return a symbolic expression representing the result of the 
        differentiation given a level of differentiation
        """
        quotient_denom = (self.right * self.right)
        quotient_num = (self.right * self.left.deriv(level)) - (self.left * self.right.deriv(level))
        return quotient_num / quotient_denom

    def eval(self, mapping):
        """
        Evaluates expressions for particular values of variables where mapping 
        is a dictionary mapping variable names to values
        """
        return self.left.eval(mapping) / self.right.eval(mapping)


class Mul(BinOp):
    """
    A subclass to represent Multiplication with both a symbol to represent how
    it is mathematically shown and a value to determined its precedence in 
    the PEMDAS rules of order of operations.
    """
    sym = '*'
    preced = 1

    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the left and right peices of a certain expression. Inherits
        these from the super() class of BinOp
        """
        super().__init__(left, right)

    def __str__(self):
        """
        Accounts for the representation of the class's operation, including 
        how it needs to be represented with certain parenthesization 
        requirements
        """
        left_part = str(self.left)
        right_part = str(self.right)
        if self.left.sym is not None:
            if self.left.preced == 0:
                left_part = '(' + left_part + ')'
        if self.right.sym is not None:
            if self.right.preced == 0:
                right_part = '(' + right_part + ')'
        sym = ' ' + self.sym + ' '
        exp = left_part + sym + right_part
        return exp

    def __repr__(self):
        """
        Produces something that can actually be fed back into python but 
        essentially represents the way in which one should call the method
        in a different context/a way to represent the function in a Python-
        friendly way
        """
        exp = "Mul(" + repr(self.left) + ", " + repr(self.right) + ")"
        return exp

    def simplify(self):
        """
        Simplify should take no arguments, and it should return a simplified 
        form of the expression that also follows all mathematical rules such as 
        order of operations, etc.
        """
        right = self.right.simplify()
        left = self.left.simplify()
        if type(left) == Num and type(right) == Num:
            return Num(left.n * right.n)
        if type(left) == Num and left.n == 0:
            return Num(0)
        if type(right) == Num and right.n == 0:
            return Num(0)
        if type(left) == Num and left.n == 1:
            return right
        if type(right) == Num and right.n == 1:
            return left
        return left * right

    def deriv(self, level):
        """
        This method should take a single argument (a string containing the name 
        of the variable with respect to which we are differentiating), and it 
        should return a symbolic expression representing the result of the 
        differentiation given a level of differentiation
        """
        return self.left * self.right.deriv(level) + self.right * self.left.deriv(level)

    def eval(self, mapping):
        """
        Evaluates expressions for particular values of variables where mapping 
        is a dictionary mapping variable names to values
        """
        return self.left.eval(mapping) * self.right.eval(mapping)


if __name__ == '__main__':
    x = Add(2, 3)
    mapping = {Num(2): 2, Num(3): 3}
    answer = x.eval(mapping)
    print(answer)
    
    pass
