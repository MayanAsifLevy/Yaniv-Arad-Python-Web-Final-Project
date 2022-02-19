from pymongo import MongoClient
from bson import ObjectId

class Mongo_employee:
    def __init__(self):
        self.__mongo_client=MongoClient(port=27017)
        self.__db=self.__mongo_client['proj2_Factory']

    def get_employee_data(self):
        employees=[]
        recrods= self.__db['employees'].find({})
        for r in recrods:
            rec={}
            rec["emp_id"]=str(r["_id"])
            rec["First_Name"]=(r["First_Name"])
            rec["Last_Name"]=r["Last_Name"]
            rec["Start_Work_Year"]=r["Start_Work_Year"]
            rec["Department_id"]=str(r["Department_id"])

            employees.append(rec)
        return employees

    def add_employee(self, obj):
        self.__db['employees'].insert_one(obj)

    def update_employee(self, id,updated_emp):
         self.__db["employees"].update_one({'_id' :ObjectId(id) } , {"$set" : updated_emp} )


    def delete_emp(self, id):
        self.__db["employees"].delete_one({'_id' : ObjectId(id) })