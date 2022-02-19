from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import json
from bson import ObjectId, datetime
from Server.BL.auth_bl import AuthBL
from Server.BL.emp_bl import Employees
from Server.BL.dep_bl import Departments
from Server.BL.shift_bl import Shifts
from Server.BL.users_bl import Users

app = Flask(__name__)
CORS(app)


class MyEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance(self, ObjectId) or isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return str(obj)
        return super(MyEncoder, self).default(obj)

app.json_encoder=MyEncoder


auth_bl=AuthBL()
emp_bl=Employees()
dep_bl=Departments()
shift_bl=Shifts()
users_bl=Users()


@app.route('/auth/login',methods=['POST'])
def login():
    username = request.json["username"]
    email = request.json["email"]
    token = auth_bl.get_token(username,email)
    if token!=-1:
        return token
    else:
        return jsonify(-1)


@app.route('/auth/login',methods=['GET'])
def get_user_name():
    user_name= auth_bl.token_verification(is_login=1)
    if user_name == "not authorized":
        return jsonify("you are not authorized")
    else:
        if user_name == "no actions left":
            return jsonify("no actions left")
        else:
            return jsonify(user_name)



@app.route('/employees', methods= ['GET'])
def get_employees():
    user_name=auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        dep_name = request.args.get('dep') # for the department filter
        emps, dep, shift_list=emp_bl.get_employees(dep_name)
        return jsonify(emps, dep, shift_list)


@app.route('/employees/<string:id>', methods= ['GET'])
def get_employee(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        emp, dep_list, emps_with_deps_shifts,shift_list, =emp_bl.get_employee(id)
        return jsonify(emp, dep_list, emps_with_deps_shifts, shift_list)


@app.route('/employees/<string:id>', methods= ['PUT'])
def update_employee(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        emp_bl.update_employee(id, data)
        return jsonify("updated")
    

@app.route('/employees', methods= ['POST'])
def add_employee():
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        emp_bl.add_employee(data)
        return jsonify("added")


@app.route('/employees/<string:id>', methods= ['DELETE'])
def delete_employee(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        emp_bl.delete_employee(id)
        return jsonify("deleted")
    

@app.route('/departments', methods= ['GET'])
def get_departments():
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:    
        list_emps_in_dep, emps=dep_bl.get_departments()
        return jsonify(list_emps_in_dep, emps)
    


@app.route('/departments/<string:id>', methods= ['GET'])
def get_department(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        dep_to_update_details , avail_emp_data, emps = dep_bl.get_department(id)
        return jsonify(dep_to_update_details , avail_emp_data, emps)
    


@app.route('/departments', methods= ['POST'])
def add_department(): 
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        dep_bl.add_department(data)
        return jsonify("added")
    


@app.route('/departments/<string:id>', methods= ['PUT'])
def update_department(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        dep_bl.update_department(id, data)
        return jsonify("updated")
    


@app.route('/departments/<string:id>', methods= ['DELETE'])
def delete_department(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        dep_bl.delete_department(id)
        return jsonify("deleted")
    


@app.route('/shifts', methods= ['GET'])
def get_shifts():
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        shift_data, all_emps=shift_bl.get_shifts_and_emp()
        return jsonify(shift_data, all_emps)
   


@app.route('/shifts/<string:id>', methods= ['PUT'])
def update_shifts(id):
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        shift_bl.get_update_shifts(id,data)
        return jsonify("updated")
  


@app.route('/shifts', methods= ['POST'])
def add_shifts_and_emps():
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        data = request.json
        if data["type"]=="save_add_emp":
            shift_bl.add_shifts_and_emps(data)
            return jsonify("updated")
        if data["type"]=="add_shift":           
            new_shift_id=shift_bl.add_shift(data)
            return jsonify(new_shift_id)
    
@app.route('/users',methods=['GET'])
def get_users():
    user_name= auth_bl.token_verification(is_login=0)
    if user_name == "no actions left":
        return jsonify("no actions left")
    else:
        users_list=users_bl.get_users_data()
        return jsonify(users_list)


app.run()
