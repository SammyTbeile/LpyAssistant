## LPyAssistant

A simple python LP solver

### Usage:
LPyAssistant can either be run on a local file or as a Flask app:

### Flask app
Run using:
```
FLASK_APP=lpyassistant poetry run flask run
```
### Local File
Create a file containing your LP in the followin format:
```
Minimize/Maximize
objective_function
Subject to
Constraint 1
Constraint 2
...
```
Then solve using `poetry run file $FILENAME`
