from bson import ObjectId

from Server.DAL.Emp_DAL import Mongo_employee
from Server.DAL.Dep_DAL import Mongo_department
from Server.DAL.Shifts_DAL import Mongo_Shifts
from Server.DAL.Shift_emp_DAL import Mongo_emp_shift

class Employees:
    def __init__(self):
        self.emp_dal=Mongo_employee()
        self.dep_dal=Mongo_department()
        self.shift_dal=Mongo_Shifts()
        self.emp_shift_dal=Mongo_emp_shift()
  
  
    def get_employees(self, dep_name):
        emps=self.emp_dal.get_employee_data()
        deps= self.dep_dal.get_departments_data()
        shifts_per_emp=self.emp_shift_dal.get_emp_shift()
        shft=self.shift_dal.get_shifts_data()

        emps_with_deps_shifts=[]
        
         # for each employee get its data
        for e in emps:
            emp_dep={}
            emp_dep["FullName"] = e["First_Name"]+ " " +e["Last_Name"]
            emp_dep["emp_id"]=e["emp_id"]

            arr_dep= list(filter(lambda x: x["dep_id"]==e["Department_id"],deps))
            if len(arr_dep)>0:
                emp_dep["Department"] = arr_dep[0]["Name"]
                emp_dep["Department_id"] = e["Department_id"]

            arr_emp_shifts= list(filter(lambda x: x["emp_id"]==e["emp_id"],shifts_per_emp))
            emp_dep["shifts"]=[]
            if len(arr_emp_shifts)>0:
                
                for es in arr_emp_shifts:
                    arr_shifts= list(filter(lambda x: x["_id"]==es["shift_id"],shft))
                    if len(arr_shifts)>0:     
                        emp_dep["shifts"].append(arr_shifts[0])
            
            emps_with_deps_shifts.append(emp_dep)

        if dep_name is not None:
            filtered_emps= list(filter( lambda x: x["Department"]== dep_name,emps_with_deps_shifts))
            emps_with_deps_shifts=filtered_emps

        return emps_with_deps_shifts, deps, shft 


    def add_employee(self, obj):
        add_object = {"First_Name" : obj["fName"], "Last_Name" : obj["lName"], "Start_Work_Year" : int(obj["Start_work_year"]) , "Department_id": ObjectId(obj["department_id"]) }
        self.emp_dal.add_employee(add_object)
         

    def get_employee (self, id):
        emps_with_deps_shifts, dep_list , shft  =self.get_employees(None)
        for emp_shift in emps_with_deps_shifts:
            if emp_shift["emp_id"]==id:
                emps_with_deps_shifts=emp_shift
                
                break   
        emps=self.emp_dal.get_employee_data()
        for e in emps:
            emp={}
            if e["emp_id"]== id:
                emp=e

                # to find the shifts (from shft)  that that are NOT avaiable in emps_with_deps_shifts
                shifts_id_list=[]
                for s in shft:
                    shifts_id_list.append(s["_id"])

                emp_shift_id_list=[]
                for i in emps_with_deps_shifts["shifts"]:
                    emp_shift_id_list.append(i["_id"])
                
                
                avail_s_list=[x for x in shifts_id_list if x not in emp_shift_id_list]
                #in order to find all the shifts data in order to present it as avaiable for the employee
                avail_shifts_for_emp=[]
                for a in avail_s_list:
                   av=list(filter(lambda x: x["_id"]==a,shft))
                   avail_shifts_for_emp.append(av[0])
              
              # provide only the shifts that can be added to the employee
                # avail_shifts_for_emp   
                break
                
        
        return emp, dep_list, emps_with_deps_shifts, avail_shifts_for_emp


    def update_employee(self, id, obj):
        updated_emp = {}
        updated_emp["First_Name"] = obj["First_Name"]
        updated_emp["Last_Name"] = obj["Last_Name"]
        updated_emp["Start_Work_Year"] = int(obj["Start_work_year"])
        updated_emp["Department_id"] = ObjectId(obj["Department_ID"])

        self.emp_dal.update_employee(id,updated_emp ) 
        
        for s in obj['add_shifts_to_emp']:
            update_shift_emp = {}
            update_shift_emp["emp_id"]= ObjectId(id)
            update_shift_emp["shift_id"]= ObjectId(s)
            a=update_shift_emp
            self.emp_shift_dal.insert_shift_emp(update_shift_emp)
       

    def delete_employee(self, emp_id):
        self.emp_shift_dal.delete_emp_shift(emp_id)
        self.emp_dal.delete_emp(emp_id)



