from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash



class Employee(UserMixin, db.Model):
    # verbose plural
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), index=True)
    last_name = db.Column(db.String(50), index=True)
    date_of_birth = db.Column(db.DateTime)
    date_of_first_appointment = db.Column(db.DateTime)
    next_of_kin = db.Column(db.String(50), index=True)
    department_name = db.Column(db.String(50), db.ForeignKey('departments.name'))
    educational_qualification = db.Column(db.String(60))
    role_name = db.Column(db.String(60), db.ForeignKey('roles.name'))
    address = db.Column(db.String(80))
    phone_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    marital_status = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    current_status = db.Column(db.String(60))
    
    
    # Prevent password from being assessed
    @property
    def password(self):
        raise AttributeError("Passowrd is Hidden")
    
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username








# sets up the user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(300))
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __repr__(self):
        return self.name


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(300))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return self.name






    

    



