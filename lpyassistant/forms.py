from flask_wtf import FlaskForm, csrf
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class LPForm(FlaskForm):
    """LP Form"""
    minimize = SelectField(
        u'Minimize?',
        choices = [
            ('minimize','minimize'),
            ('maximize','maxmize')
        ],
        validators=[DataRequired()]
    )
    objective = StringField(
        u'Objective Function:',
        validators=[DataRequired()]
    )
    constraints = TextAreaField(
        u'Subject To (separate constraints with a new line):',
        validators=[DataRequired()]
    )
    submit = SubmitField('Calculate')
