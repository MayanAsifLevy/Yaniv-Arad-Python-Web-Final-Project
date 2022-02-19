from pymongo import MongoClient
import datetime
from bson import ObjectId


class Mongo_Shifts:
    def __init__(self):
        self.__Mongo_client = MongoClient(port=27017)
        self.__db = self.__Mongo_client['proj2_Factory']

    def get_shifts_data(self):
        shifts=[]
        recrods= self.__db['shifts'].find({})
        for r in recrods:
            rec={}
            rec["_id"]= str(r["_id"])
            rec["Date"] = datetime.date(r["Date"].year, r["Date"].month, r["Date"].day)
            rec ["Starting_hour"]=r["Starting_hour"]
            rec ["Ending_hour"]=r["Ending_hour"]
            shifts.append(rec)

        return shifts

    
    
    def add_shift(self, obj):
        new_shift_id=self.__db['shifts'].insert_one(obj)
        return new_shift_id.inserted_id

    def update_shift(self, shift_id, update_shift):
        self.__db["shifts"].update_one({'_id' :ObjectId(shift_id) } , {"$set" : update_shift} )

