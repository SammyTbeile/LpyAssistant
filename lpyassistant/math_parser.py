from pulp import *
import re
import operator

def parse_expression(expression: str, model_vars: dict, constraint: bool=True):
    expr = LpAffineExpression() if not constraint else LpConstraint()
    # Get list of vars
    var_regex = re.compile(r'[a-zA-Z]_?\d?')
    var_regex_list = var_regex.findall(expression)
    var_list = list(map(lambda x: LpVariable(name=x,lowBound=0),var_regex_list))
    # For each var, find constants
    for var in var_list:
        if var.name in model_vars:
            var = model_vars.get(var.name)
        else:
            model_vars[var.name] = var
        test= re.search(f'(-?)\s*(\d*){var.name}',expression)
        constant = 1
        if(test.group(2) != ''):
            constant = int(test.group(2))
        if(test.group(1) != ''):
            constant *= -1
        expr += operator.mul(constant,var)
    # Parse for constants
    constant_regex = re.compile(r'[^a-zA-Z_](-?\d+)[^a-zA-Z].*=')
    constant_list = constant_regex.findall(expression)
    for constant in constant_list:
        expr += int(constant)

    # Get constraining
    if constraint:
        expr_regex = re.compile(r'([><=])(=?)\s*(-?)(\d+)')
        expr_eq = expr_regex.search(expression)
        expr_constant = int(expr_eq.group(4))
        if(expr_eq.group(3)):
            expr_constant *= -1
        if(expr_eq.group(1) == '='):
            expr = expr == expr_constant
        elif(expr_eq.group(1) == '>' and expr_eq.group(2) == '='):
            expr = expr >= expr_constant
        elif(expr_eq.group(1) == '<' and expr_eq.group(2) == '='):
            expr = expr <= expr_constant
    return (expr,model_vars)

    



#print(parse_expression('2x + y -50<= 20',{}))
#print(parse_expression('-4x+5y >=10',{}))
#print(parse_expression('-x - 2y >= -2',{}))
#print(parse_expression('-x + 5y = 15',{}))
#print(parse_expression('-x + 5y + 50 = 15',{}))
#print(parse_expression('-x + 5y -50 = 15',{}))
#print(parse_expression('x+2y',constraint=False))
