"""
Solutions to module 4 - A calculator
Student: 
Mail:
"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class CalculatorSyntaxError is complete as well as handling in main
of CalculatorSyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA4tokenizer import TokenizeWrapper

def fib(n):
    if  n < 0 or not n.is_integer():
        raise EvaluationError(f"Argument to fib is {n}. Must be integer >=0")
    n = int(n)

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


functions_1 = {"sin": math.sin,
               "cos": math.cos,
               "exp": math.exp,
               "log": math.log,
               "fac": math.factorial,
               "fib": fib}

class CalculatorSyntaxError(Exception):
    pass

class EvaluationError(Exception):
    pass


def statement(wtok, variables):
    result = assignment(wtok, variables)

    if not wtok.is_at_end():
        raise CalculatorSyntaxError("Unexpected token")

    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    while wtok.get_current() == "=":
        wtok.next()
        if not wtok.is_name():
            raise CalculatorSyntaxError("Expected variable after '='")
        name = wtok.get_current()
        variables[name] = result
        wtok.next()
    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':
        wtok.next()
        if wtok.get_previous() == '+':
            result = result + term(wtok, variables)
        else: # wtok.get_previous() == '-'   
            result = result - term(wtok, variables)
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/': 
        wtok.next()

        if wtok.get_previous() == '*':
            result = result * factor(wtok, variables)

        else: # wtok.get_previous() == '/'   
            denominator = factor(wtok, variables)

            if denominator == 0:
                raise EvaluationError("Division by zero")
            result = result / denominator

    return result


def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(':
        try:
            wtok.next()
            result = assignment(wtok, variables)

            if wtok.get_current() != ')':
                if wtok.line.count('(') > wtok.line.count(')'):
                    raise CalculatorSyntaxError("Unbalanced parentheses")
                else:
                    raise CalculatorSyntaxError("Expected ')'")

            wtok.next()

        except TokenError:
            raise CalculatorSyntaxError("Unbalanced parentheses")

    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-':
        wtok.next()
        result = -(factor(wtok, variables))

    elif wtok.get_current() in functions_1:

            
            function_name = wtok.get_current()

            
            # check bracket
            wtok.next()
            if wtok.get_current() != '(':
                raise CalculatorSyntaxError("Expected '('")
    
            # check the argument number
            wtok.next()
            argument = assignment(wtok, variables) # assignment involves wtok.next()
    
            # check bracket
            if wtok.get_current() != ')':
                raise CalculatorSyntaxError("Expected ')'")

            if function_name == "fac":
                if argument < 0 or not argument.is_integer():
                    raise EvaluationError(f"Argument to fac is {argument}. Must be integer >= 0")
                argument = int(argument)

            if function_name == "log" and argument <= 0:
                raise EvaluationError("Argument to log must be positive")

            wtok.next()
            result = functions_1[function_name](argument)

    elif wtok.is_name():
        if wtok.get_current() not in variables:
            raise EvaluationError(f"Undefined variable: {wtok.get_current()}")
        name = wtok.get_current()
        result = variables[name]
        wtok.next()

    

    else:
        raise CalculatorSyntaxError("Expected number or '('")  
    return result


         
def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"PI": math.pi,
                 "E": math.e,
                 "ans": 0.0}
    
    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0]=='#':
            continue
        
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        elif wtok.get_current() == 'vars':
            for name, value in variables.items():
                print(name,  ":", value)
        else:
            try:
                result = statement(wtok, variables)
                variables["ans"] = result
                print('Result:', result)

            except CalculatorSyntaxError as se:
                print("*** Syntax error: ", se)
                if wtok.is_newline():
                    current = "*EOL*"
                else:
                    current = wtok.get_current()
                print(
                f"Error occurred at '{current}' just after '{wtok.get_previous()}'")

            except EvaluationError as ee:
                print("*** Evaluation error:", ee)
            
            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
                print(f"*** The error occurred at token '{wtok.get_current()}' just after token '{wtok.get_previous()}'")
 


if __name__ == "__main__":
    main()
