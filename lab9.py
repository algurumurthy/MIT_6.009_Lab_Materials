#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:51:45 2020

@author: ananyagurumurthy
"""

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
def help_space(string):
    """
    Spaces the string out for all required amounts of space for the parse 
    function
    """
    spaced_string1 = string.replace(")", " ) ")
    spaced_string2= spaced_string1.replace("(", " ( ")
    spaced_string3 = spaced_string2.replace("\n", " \n ")
    return spaced_string3

def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    """
    new_spaced_string = help_space(source)
    
    if "\n" not in new_spaced_string:
        
        new_spaced_string = [new_spaced_string]
        
    else:
        
        new_spaced_string = new_spaced_string.split("\n")
        
    for x in range(len(new_spaced_string)):
        
        if ";" in new_spaced_string[x]:
            
            new_spaced_string[x] = new_spaced_string[x][:new_spaced_string[x].index(";")]
            
    new_spaced_string = "".join(new_spaced_string)
    
    return new_spaced_string.split()



def checker(var):
    """
    This accounts for the situation in which the variable inputted is not 
    necessarily a float or an int and returns the right type accordingly based
    on try and accept statements
    """
    try:
        return int(var)
    except:
        try:
            return float(var)
        except:
            return var

def help_parse(tokens, parse_index):   
    """
    Helper function for the parse function wherein it utilizes a the tokens and
    an index to begin with in order to parse an entire set of tokens into
    something more readable in a list.
    """
    if tokens[parse_index] == ')':
        
        raise SnekSyntaxError
        
    if tokens[parse_index] != '(':
        
        return (checker(tokens[parse_index]), parse_index +1)
    
    else:
        
        output = []
        
        parse_index = parse_index + 1
        
        if tokens[parse_index] == ')':
        
            return (output, parse_index+1)
        
        tracker = parse_index
        
#        expression, tracker = help_parse(tokens, parse_index)
#        output.append(expression)
        while tokens[parse_index] != ')':
        
            expression, tracker = help_parse(tokens, parse_index)
            
            output.append(expression)
            
            parse_index = tracker
            
#            if tokens[parse_index] == ')':
#                break
            if parse_index >= len(tokens):
                
                break
            
        print('TOKENS', tokens)
        
        if output[0] == 'lambda' and not (len(output) == 3 and isinstance(output[1], list)):
            
            raise SnekSyntaxError
            
        if output[0] == "lambda" and isinstance(output[1], list):
            
            for element in output[1]:
                
                if not isinstance(checker(element), str):
                    
                    raise SnekSyntaxError
                    
        if output[0] == "define" and len(output) != 3:
            
            raise SnekSyntaxError
            
        if output[0] == "define" and not (isinstance(output[1], list) or isinstance(output[1], str)):
            
            raise SnekSyntaxError
            
        if output[0] == "define" and isinstance(output[1], list) and len(output[1]) == 0:
            
            raise SnekSyntaxError
            
        if output[0] == "define" and isinstance(output[1], list):
            
            for element in output[1]:
                
                if not isinstance(checker(element), str):
                    
                    raise SnekSyntaxError
                    
        return (output, tracker+1)
    

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    if tokens.count('(') != tokens.count(')'):
        
        raise SnekSyntaxError
        
    snek_exp, ind = help_parse(tokens, 0)
    
    print(snek_exp)
    
    if ind == len(tokens):
        
        return snek_exp
    
    else:
        
        print(snek_exp)
        
        raise SnekSyntaxError


######################
# Built-in Functions #
######################

def multiply(mlist):
    """
    Multipliies all of the numbers into a product from the given list
    """
    product = 1
    for num in mlist:
        product = product * num
    return product

def divide(dlist):
    """
    Divides all of the numbers into a quotient from the given list
    """
    quotient = dlist[0]
    for num in dlist[1:]:
        quotient = quotient / num
    return quotient

    """
    All of the builtin types for the language as intstructed in the lab file
    """
snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': multiply,
    '/': divide,
}

class Environments():
    """
    A class that defines what an environment is, which consists of bindings 
    from variable names to values, and possibly a parent environment, from 
    which other bindings are inherited
    """
    def __init__(self, variables = None, parent = None):
        """
        Constructor to represent all of the built in variables and whether or 
        not it belongs to a parent class
        """
        if variables is None:
            self.variables = {}
        else:
            self.variables = variables
        self.parent = parent
        
    def __setitem__(self, key, value):
        """
        Sets the value of the variable at a particular key to a specified
        value
        """
        self.variables[key] = value
        
    def __getitem__(self, key):
        """
        Retrieves the value of the variable from a particular key and returns
        it
        """
        if key in self.variables.keys():
            return self.variables[key]
        elif self.parent is None:
            raise SnekNameError
        else:
            return self.parent[key]
        
    def parse_tracker(self, key):
        """
        Given a certain parsing through a function, tracks how far through the
        function we want to retrieve something from a certain key
        """
        if key in self.variables.keys():
            return self
        else:
            return self.parent.parse_tracker(key)

#Creates a Snek class from Environment that inherits all of the previously
#described Snek builtins from above
Snek = Environments(None)
Snek.variables = snek_builtins
        
class Functions:
    """
    Class to account for how to define and use user-defined functions and 
    values
    """
    def __init__(self, parameters, expression, parent = Snek):
        """
        Constructor to account for the three peices of any function: a set of
        parameters, an expression and whether or not there is a parent class,
        which in this case would be Snek
        """
        self.expression = expression
        self.parameters = parameters
        self.parent = parent
        
    def __call__(self, parameter):
        """
        Responds to the case in which the user-defined function gets called at
        any point in time
        """
        if len(parameter) != len(self.parameters):
            raise SnekEvaluationError
        env = Environments(parent = self.parent)
        for index in range(len(parameter)):        
            env[self.parameters[index]] = parameter[index]
        return evaluate(self.expression, env)

    
##############
# Evaluation #
##############

def evaluate(tree, environment = None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if environment is None:
        
        environment = Environments(parent = Snek)
        
    if type(tree) == float or type(tree) == int:
        
        return tree
    
    if type(tree) != list and type(tree) == str:
        
        value = environment[tree]
        
        return value
    
    if tree[0] == 'lambda':
        
        function = Functions(tree[1], tree[2], environment)
        
        return function
    
    elif tree[0] == 'define':
        
        if len(tree) != 3:
            
            raise SnekEvaluationError
            
        if type(tree[1]) != list:
            
            environment[tree[1]] = evaluate(tree[2], environment)
            
            return environment[tree[1]]
        
        else:
            
            function = Functions(tree[1][1:], tree[2], environment)
            
            environment[tree[1][0]] = function
            
            return environment[tree[1][0]]
        
    else:
        
        try:
            
            final_tree = []
            
            variables = tree[1:]
            
            for index, item in enumerate(variables):
                
                final_tree.append(evaluate(variables[index], environment))
                
            function = evaluate(tree[0], environment)
            
            if not callable(function): 
                
                raise SnekEvaluationError
                
            return function(final_tree)
        
        except NameError:
            
            raise SnekNameError
            

def result_and_env(tree, environment = None):
    """
    Takes the same arguments as evaluate but returns a tuple with two elements: 
    the result of the evaluation and the environment in which the expression 
    was ultimately evaluated
    """
    if environment is None:
        environment = Environments(parent = Snek)
    return (evaluate(tree, environment), environment)


def repl():
    """
    REPL (a "Read, Evaluate, Print Loop") for Snek. A REPL has a simple job: 
    it continually prompts the user for input until they type QUIT
    """
    env = Environments(parent = Snek)
    while True:
        source = input('in> ')
        print(env.variables)
        if source == 'QUIT':
            break
        try:
            print(evaluate(parse(tokenize(source)), env))
        except SnekError as e:
            print(e)


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
#    repl()
#    print(parse(tokenize(('lambda () 2'))))
#    env = Environments(parent = Snek)
#    source = parse(tokenize('(define square (lambda (x) (* x x)))'))
#    one = evaluate(source, env)
#    func = parse(tokenize('(square 21)'))
#    two = evaluate(func, env)
#    print(one, two)
#    print
    pass
