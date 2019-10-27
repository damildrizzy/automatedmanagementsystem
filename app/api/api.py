from flask import request, jsonify
from flask_restful import Resource
from app.models import Employee, Role, Department
from app import db, ma


class EmployeeSchema(ma.ModelSchema):
    class Meta:
        model = Employee


class DepartmentSchema(ma.ModelSchema):
    class Meta:
        model = Department


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


employees_schema = EmployeeSchema(many=True)
employee_schema = EmployeeSchema()
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class EmployeeListResource(Resource):


    def get(self):
        employees = Employee.query.all()
        employees = employees_schema.dump(employees)
        return {'status': 'success', 'data': employees}
 
    def post(self):
        json_data = request.get_json()
        
        if not json_data:
            response = {'error': 'No Input Data Provided'}
            return jsonify(response), 400

        employee = Employee.query.filter(
                        Employee.email == json_data['email']).first()
        if employee:
            return {'message': 'Employee with that email already exists'}
        employee = Employee(
                            date_of_first_appointment=json_data['date_of_first_appointment'],
                            email=json_data['email'],
                            first_name=json_data['first_name'],
                            last_name=json_data['last_name'],
                            password=json_data['password'],
                            date_of_birth=json_data['date_of_birth'],
                            next_of_kin=json_data['next_of_kin'],
                            educational_qualification=json_data['educational_qualification'],
                            address=json_data['address'],
                            phone_number=json_data['phone_number'],
                            marital_status=json_data['marital_status'])
        db.session.add(employee)
        db.session.commit()

        result = employee_schema.dump(employee)
        return{'status': 'success', 'data': result}, 201


class EmployeeResource(Resource):
    def get(self, id):
        employee = Employee.query.get_or_404(id)
        employee = employee_schema.dump(employee)
        return {'status': 'success', 'data': employee}
    


class DepartmentListResource(Resource):
    def get(self):
        departments = Department.query.all()
        departments = departments_schema.dump(departments)
        return {'status': 'success', 'data': departments}

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No Input Data Provided'}, 400
        # validate and deserialize input
        data = department_schema.load(json_data)
        
        department = Department.query.filter(Department.name == json_data['name']).first()
        if department:
            return {'message': 'Department with that name already exists'}
        department = Department(name=json_data['name'], description=json_data['description'])
        db.session.add(department)
        db.session.commit()

        result = department_schema.dump(department)

        return {'status': 'success', 'data': result}, 201


class DepartmentResource(Resource):
    def get(self, id):
        department = Department.query.get_or_404(id)
        department = department_schema.dump(department)
        return {'status': 'success', 'data': department}

    def put(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No Input Data Provided'}, 400

        department = Department.query.get_or_404(id)

        department.name = json_data['name']
        department.description = json_data['description']
        db.session.commit()

        result = department_schema.dump(department)

        return {'status': 'success', 'data': result}    

    def delete(self, id):        
        department = Department.query.get_or_404(id)
        if not department:
            return {'message': 'Department does not exist'}
        db.session.delete(department)
        db.session.commit()
        result = department_schema.dump(department)
        return {'status': 'success', 'data': result}


class RoleListResource(Resource):
    def get(self):
        roles = Role.query.all()
        roles = roles_schema.dump(roles)
        return {'status': 'success', 'data': roles}

    def post(self):
        json_data = request.get_json(force=True)
        
        if not json_data:
            return {'message': 'No Input Data Provided'}, 400

        role = Role.query.filter(name=json_data['name']).first()
        if role:
            return {'message': 'Role with that name already exists'}
        role = Role(name=json_data['name'], description=json_data['description'])
        db.session.add(role)
        db.session.commit()

        result = role_schema.dump(role)

        return {'status': 'success', 'data': result}, 201


class RoleResource(Resource):
    def get(self, id):
        role = Role.query.get_or_404(id)
        role = role_schema.dump(role)
        return {'status': 'success', 'data': role}

    def put(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No Input Data Provided'}, 400
        
        role = Role.query.get_or_404(id)
        if not role:
            return {'message': 'Role does not exist'}, 400
        role.name = json_data['name']
        role.description = json_data['description']
        db.session.commit()

        result = role_schema.dump(role)

        return {'status': 'success', 'data': result}, 201

    def delete(self, id):
        role = Role.query.get_or_404(id)
        if not role:
            return {'message': 'role does not exist'}
        db.session.delete(role)
        db.session.commit()
        result = role_schema.dump(role)
        return {'status': 'success', 'data': result}, 201
