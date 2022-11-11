from wtforms import Form, BooleanField, StringField, PasswordField
from wtforms.validators import Email, InputRequired, EqualTo, DataRequired, Length
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    email= StringField(
        'Email', render_kw={'placeholder':'Email'},validators=[DataRequired(), Email()])
    password= PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8, max=30)], render_kw={'placeholder':'Password'})
    confirm  = PasswordField('Repeat Password', render_kw={'placeholder':'Repeat Password'}, validators=[InputRequired()])