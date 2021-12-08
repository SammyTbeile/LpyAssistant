from flask import current_app as app
from flask import Flask, render_template, redirect, url_for
from flask_wtf import csrf
import urllib
from .forms import LPForm
from .solver import pulp_solve

#app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    form = LPForm()
#    csrf.generate_csrf()
    if form.validate_on_submit():
       minimize = (form.minimize.data == 'minimize')
       obj_func = form.objective.data
       constraints = form.constraints.data.splitlines()
       print("solving")
       solution = pulp_solve(minimize=minimize,objective_function=obj_func,constraints=constraints)
       print("solved")
       return redirect(url_for('solution', solution=urllib.parse.quote_plus(solution)))
    else:
       print(form.errors)
       print("Form error")


    return render_template('index.html', form=form)

@app.route('/solution/<solution>')
def solution(solution):
    return render_template('solution.html',solution=urllib.parse.unquote_plus(solution))

if __name__ == "__main__":
    app.run()
