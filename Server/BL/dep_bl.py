from bson import ObjectId

from Server.DAL.Emp_DAL import Mongo_employee
from Server.DAL.Dep_DAL import Mongo_department
from Server.DAL.Shifts_DAL import Mongo_Shifts
from Server.DAL.Shift_emp_DAL import Mongo_emp_shift


class Departments:
    def __init__(self):
        self.emp_dal=Mongo_employee()
        self.dep_dal=Mongo_department()
        self.shift_dal=Mongo_Shifts()
        self.emp_shift_dal=Mongo_emp_shift()


    def  get_departments(self):
        deps= self.dep_dal.get_departments_data()
        emps=self.emp_dal.get_employee_data()

        # get the list of deps and their employees
        list_emps_in_deps=[]
        for d in deps:
            list_emps_in_dep={}
            list_emps_in_dep["dep_details"]= d
            list_emps_in_dep["emps_in_dep"]=list(filter(lambda x: x['Department_id']==d['dep_id'],emps))
            list_emps_in_dep["manager_info"] = list(filter(lambda x: x['emp_id']==d['manager_id'],emps))
            
            list_emps_in_deps.append(list_emps_in_dep)

        return list_emps_in_deps,emps

    def  get_department(self, id):
        list_emps_in_deps,emps=self.get_departments()
        for d in list_emps_in_deps:
            dep_to_update_details={} 
            if d["dep_details"]["dep_id"]==id:
                dep_to_update_details=d # all deatils about sepecific deparatmanet that we want to update
                break

        emps_already_in_dep=list(map(lambda x: x["emp_id"], dep_to_update_details["emps_in_dep"]))
        all_emps=list(map(lambda x: x["emp_id"], emps))
        emp_2b_added_to_dep_list=[x for x in all_emps if x not in emps_already_in_dep]

        #to get the avaiable emp details:
        avail_emp_data=[]
        for e in emp_2b_added_to_dep_list:
                av=list(filter(lambda x: x["emp_id"]==e,emps))
                avail_emp_data.append(av[0])
        return  dep_to_update_details , avail_emp_data ,emps
     
        
    def add_department(self, obj):
        add_object = {"Name" : obj["dName"], "Manager_id" : ObjectId(obj["dManager_id"])}
        self.dep_dal.add_department(add_object)


    def update_department(self, id, obj):
        if  obj["type"]== "update_dep":
            updated_dep={}
            updated_dep["Name"]= obj["Department_Name"]
            updated_dep["Manager_id"]=ObjectId(obj["Manager_id"])
        
            self.dep_dal.update_department(id,updated_dep ) 

            
        if obj["type"]== "add_emp_to_dep":
                     
            update_emp={}
            update_emp["Department_id"]=ObjectId(id)
            
            self.emp_dal.update_employee( ObjectId(obj["emp_id"]),update_emp)


            
    def delete_department(self,dep_id):
        self.dep_dal.delete_department(dep_id) 

        emps=self.emp_dal.get_employee_data()
        delete_emp=list(filter(lambda x: x['Department_id']==dep_id,emps))

        for e in delete_emp:
            self.emp_shift_dal.delete_emp_shift(e["emp_id"])
            self.emp_dal.delete_emp(e["emp_id"])
      
      
    
    

            