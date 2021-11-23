import re
import argparse
import sys
from lpyassistant.solver import pulp_solve

def main():
    parser = argparse.ArgumentParser(description='Solve an LP problem')
    parser.add_argument('file', type=str,help='a file containing the LP to solve')
    args = parser.parse_args()

    # Setup vars
    minimize = True
    obj_func = ""
    constraints = []

    file_contents = []
    #Open file
    try:
        with open(args.file,'r') as f:
            file_contents = f.readlines()
    except Exception as e:
        print(f"Couldn't read file: \n {e}")
        sys.exit(1)

    # Parse header
    header_line = file_contents[0]
    if('min' in header_line.lower()):
        minimize = True
    elif('max' in header_line.lower()):
        minimize = False
    else:
        print("First line must include 'Minimize' or 'Maximize'")
        sys.exit(1)
    # Check if objective function is on header line
    if(re.search(r'[+|-|*|/]',header_line)):
        print("Objective function must be on second line")
        sys.exit(1)

    # Parse objective function
    obj_func = max(file_contents[1].split('='),key=len)

    # Check subject to line
    if('subject to' not in file_contents[2].lower()):
        print("Third line must be 'Subject to'")
        sys.exit(1)
    # Parse constraints
    for line in file_contents[3:]:
        if(',' in line):
            print("',' are not supported")
            sys.exit(1)
        constraints.append(line.strip())

    print(pulp_solve(minimize=minimize,objective_function=obj_func,constraints=constraints))
