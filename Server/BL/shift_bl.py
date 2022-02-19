from bson import ObjectId

from Server.DAL.Emp_DAL import Mongo_employee
from Server.DAL.Dep_DAL import Mongo_department
from Server.DAL.Shifts_DAL import Mongo_Shifts
from Server.DAL.Shift_emp_DAL import Mongo_emp_shift
import datetime 


class Shifts:
    def __init__(self):
        self.emp_dal=Mongo_employee()
        # self.dep_dal=Mongo_department()
        self.shift_dal=Mongo_Shifts()
        self.emp_shift_dal=Mongo_emp_shift()


    def get_shifts_and_emp(self):
        all_shifts=self.shift_dal.get_shifts_data()
        all_emps=self.emp_dal.get_employee_data()
        emps_in_shift=self.emp_shift_dal.get_emp_shift()

        # get employee data for each shipment
        shift_data=[]
        for s in all_shifts:
            shift={}
            shift["shift_data"]=s
           
            arr_emp_in_shift= list(filter(lambda x: x["shift_id"]==s["_id"],emps_in_shift))
            emps_in_shift_list=[]
            if len(arr_emp_in_shift)>0:  
                for e in arr_emp_in_shift:
                    arr_emps= list(filter(lambda x: x["emp_id"]==e["emp_id"],all_emps))
                    if len(arr_emps)>0:  
                        emps_in_shift_list.append(arr_emps[0]) 
            shift["emp_data"]=emps_in_shift_list

             # get emps that can we added to shift
            emp_2b_added_to_shift_list=[x for x in all_emps if x not in emps_in_shift_list] 
            shift["emp_data_to_add"]=emp_2b_added_to_shift_list    
        
            shift_data.append(shift)
        return shift_data, all_emps


    def get_update_shifts(self, id, obj):
        if obj["type"]=="update_shift":
            updated_shift = {}
            updated_shift["Date"] =  datetime.datetime.strptime(obj["Date"], '%Y-%m-%d')
            updated_shift["Starting_hour"] = int(obj["Starting_hour"])
            updated_shift["Ending_hour"] = int(obj["Ending_hour"])

            self.shift_dal.update_shift(id,updated_shift ) 
            
    

    def add_shifts_and_emps(self,obj):
        # if obj["type"]=="save_add_emp":
        for o in obj["add_emps_to_shift"]:
            add_emp_to_shift={}
            add_emp_to_shift["emp_id"]=ObjectId(o)
            add_emp_to_shift["shift_id"]=ObjectId(obj["shift_id"])
            self.emp_shift_dal.insert_shift_emp(add_emp_to_shift)


    def add_shift(self, obj):
        obj["Date"]=datetime.datetime.strptime(obj["Date"], '%Y-%m-%d')
        obj["Starting_hour"]=int(obj["Starting_hour"])
        obj["Ending_hour"]=int(obj["Ending_hour"])
        new_shift_id=str(self.shift_dal.add_shift(obj))
        return new_shift_id


