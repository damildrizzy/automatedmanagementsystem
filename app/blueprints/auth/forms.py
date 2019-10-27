from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, 
                    SubmitField, ValidationError, 
                    DateTimeField, IntegerField,
                    SelectField)
from wtforms.validators import DataRequired, Email, EqualTo

from ...models import Employee


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateTimeField('Date Of Birth', format='%d/%m/%y', validators=[DataRequired()])
    next_of_kin = StringField('Next oF Kin', validators=[DataRequired()])
    date_of_first_appointment = DateTimeField('Date of First Appointment', 
                                format='%d/%m/%y', validators=[DataRequired()])
    educational_qualification = StringField('Educational Qualification', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    marital_status = SelectField('Marital Status', choices=[('Single', 'Single'), 
                                ('Married', 'Married'), ('Divorced', 'Divorced')], 
                                validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                EqualTo('confirm_password')])
    confirm_password = PasswordField('confirm_password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter(Employee.email == field.data).first():
            raise ValidationError("Sorry, Email is already in use")
    
    def validate_username(self, field):
        if Employee.query.filter(Employee.username == field.data).first():
            raise ValidationError("Sorry, This username is already taken")
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
