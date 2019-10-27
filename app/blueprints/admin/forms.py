from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ...models import Department, Role


class DepartmentForm(FlaskForm):
    # Admin can add or edit a department
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    # Admin can add or edit a department
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    # Assigns departments and roles to Employees
    department = QuerySelectField(query_factory=lambda: Department.query.all(), get_label='name')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label='name')
    current_status = SelectField('Current Status', choices=[('Employed', 'Employed'), 
                                ('Leave', 'Leave'), 
                                ('Appointment Terminated', 'Appointment Terminated'), 
                                ('Deceased', 'Deceased')])
    submit = SubmitField('Submit')


