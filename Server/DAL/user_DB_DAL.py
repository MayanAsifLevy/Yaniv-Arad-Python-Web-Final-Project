from pymongo import MongoClient
from bson import ObjectId
import datetime

class Mongo_users_DB:
    def __init__(self):
        self.__mongo_client=MongoClient(port=27017)
        self.__db=self.__mongo_client["proj2_Factory"]

    def get_user_tbl(self):
        users_db_list=[]
        users= self.__db["users"].find({})
        for u in users:
            rec={}
            rec["user_id_mongo"] =str(u["_id"])
            rec["ExternalID"]= int(u["ExternalID"])
            rec["full_name"] = u["full_name"]
            rec["maxActions"]=int(u["maxActions"])
            rec["actionAllowd_today"]=int(u["actionAllowd_today"])
            rec["currentDate"]=datetime.date(u["currentDate"].year, u["currentDate"].month, u["currentDate"].day)
            users_db_list.append(rec)
        return users_db_list

    def update_record_db(self, user_id_mongo, updated_user_data):
         self.__db["users"].update_one({'_id' :ObjectId(user_id_mongo) } , {"$set" : updated_user_data} )



    def get_one_user_from_tbl(self, id):
        u= self.__db["users"].find_one({"ExternalID":id})
        rec={}
        rec["user_id_mongo"] =str(u["_id"])
        rec["ExternalID"]= int(u["ExternalID"])
        rec["full_name"] = u["full_name"]
        rec["maxActions"]=int(u["maxActions"])
        rec["actionAllowd_today"]=int(u["actionAllowd_today"])
        rec["currentDate"]=datetime.date(u["currentDate"].year, u["currentDate"].month, u["currentDate"].day)
        return rec