from pymongo import MongoClient
from bson import ObjectId

class Mongo_department:
    def __init__(self):
        self.__mongo_client=MongoClient(port=27017)
        self.__db=self.__mongo_client['proj2_Factory']

    def get_departments_data(self):
        departments=[]
        recrods= self.__db['departments'].find({})
        for r in recrods:
            rec={}
            rec["dep_id"]=str(r["_id"])
            rec["Name"] = r["Name"]
            rec["manager_id"]=str(r["Manager_id"])
            departments.append(rec)
        return departments

    def add_department(self, obj):
        self.__db['departments'].insert_one(obj)

    def update_department(self, id, updated_dep):
        self.__db["departments"].update_one({'_id' :ObjectId(id) } , {"$set" : updated_dep} )

    def delete_department(self, dep_id):
        self.__db["departments"].delete_one({'_id' : ObjectId(dep_id) })