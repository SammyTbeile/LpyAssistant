"""Module to solve a linear programming problem

"""
from pulp import *
import re
from lpyassistant.math_parser import parse_expression

def pulp_solve(minimize: bool, objective_function: str, constraints: list):
    """ Takes in a string and uses the PuLP package to solve

    Args:
        minimize: bool on whether the function should be maximized or minimized
        objective_function: the function to max/min
        constraints: the list of constraints

    Returns:
        a string containing the solution to the LP problem
    Raises:
        ValueError: if the problem_string does not contain a Minimize or Maximize
        TypeError: if the problem_string is not a string
    """

    if type(minimize) != bool:
        raise TypeError(message='minimize is not a bool')

    if type(objective_function) != str:
        raise TypeError(message='objective_function is not a string')

    if type(constraints) != list:
        raise TypeError(message='constraints are not a list')
    
    # Define the model
    model = LpProblem(name="problem",sense=LpMinimize if minimize else LpMaximize)
    """
    if('min' in problem_string or 'Min' in problem_string):
        model = LpProblem(name="problem",sense=LpMinimize)
    elif('max' in problem_string or 'Max' in problem_string):
        model = LpProblem(name="problem",sense=LpMaximize)
    else:
        raise ValueError(message='Problem does not contain a Minimize or Maximize statement')
    """

    # Add the objective function
    obj_func,model_vars = parse_expression(objective_function,{},constraint=False)
    model +=obj_func
    

    # Add the constraints
    for constraint in constraints:
        parsed_constraint,model_vars= parse_expression(constraint,model_vars=model_vars)
        parsed_constraint.setName(f"constraint_{constraints.index(constraint)}")
        model += parsed_constraint

    # Solve
    print(model)
    status = model.solve()
    status_message = ""
    if status != 1:
        status_message = "LP cannot be solved"
        if status == -1:
            status_message += "\n LP is Infeasible"
        elif status == -2:
            status_message += "\n LP is Unbounded"
    else:
        status_message = "LP is solved optimally"
        status_message += f"\n Objective function is {'minimized' if minimize else 'maximized'} at {model.objective.value()}"
        status_message += "\n with vars:"
        for var in model.variables():
            status_message += f"\n{var.name}: {var.value()}"
    return status_message



#print(pulp_solve(minimize=False,objective_function="x+2y",constraints=["2x + y <= 20","4x-5y >= -10","-x+2y>=-2","-x+5y=15"]))

