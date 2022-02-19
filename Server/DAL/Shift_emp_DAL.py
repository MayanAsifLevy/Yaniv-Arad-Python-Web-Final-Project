from pymongo import MongoClient
from bson import ObjectId

class Mongo_emp_shift:
    def __init__(self):
        self.__mongo_client=MongoClient(port=27017)
        self.__db=self.__mongo_client['proj2_Factory']

    def get_emp_shift(self):
        emp_shifts=[]
        recrods= self.__db['shifts_per_emp'].find({})
        for r in recrods:
            rec={}
            rec["shifts_per_emp_id"] =str(r["_id"])
            rec["emp_id"]= str(r["emp_id"])
            rec["shift_id"] = str(r["shift_id"])
            emp_shifts.append(rec)
        return emp_shifts

    def insert_shift_emp(self, obj):
        self.__db["shifts_per_emp"].insert_one(obj)

    
    def delete_emp_shift(self, id):
        del_emp_id = ObjectId(id)
        
        self.__db["shifts_per_emp"].delete_many({'emp_id' : del_emp_id })
