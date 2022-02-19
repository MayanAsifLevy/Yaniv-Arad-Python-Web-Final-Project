from flask import make_response, request
import jwt
from Server.DAL.user_url_DAL import users_url_data
from Server.DAL.user_DB_DAL import Mongo_users_DB
from Server.DAL.user_json_file_DAL import UsersFile
from datetime import datetime, date

class AuthBL:
    def __init__(self):
        self.__key = "secret"
        self.__algorithm = "HS256"
        self.users_url_dal= users_url_data()
        self.user_db_dal=Mongo_users_DB()
        self.user_json_file=UsersFile()
        
    
    def get_token(self, username, email):
        user_id = self.__check_user(username,email) #verify against user url
        if user_id is not None:
            token = jwt.encode({"userid" : user_id},self.__key, self.__algorithm )
            return make_response({"token":token},200)
        else:
            return -1

    def verify_token(self, token):
        data = jwt.decode(token, self.__key, self.__algorithm)
        user_id = int(data["userid"])
        users_db_list=self.user_db_dal.get_user_tbl()
        for u in users_db_list:
            if u["ExternalID"]==user_id:  
                return True, u["full_name"] , u["ExternalID"]      
        return False,[] ,''    

    def update_user_data(self, user_data, today_datetime_as_date, user_id_mongo):
        updated_user_data=user_data
        updated_user_data["currentDate"]=today_datetime_as_date
        updated_user_data["actionAllowd_today"]=updated_user_data["maxActions"]
        del updated_user_data["user_id_mongo"]
        self.user_db_dal.update_record_db(user_id_mongo, updated_user_data)


    def check_action_left_for_user(self, user_id, is_login):
        user_data=self.user_db_dal.get_one_user_from_tbl(user_id)
        user_id_mongo=user_data["user_id_mongo"]
        today_date=date.today() ##
        today_datetime_as_date=datetime(today_date.year, today_date.month, today_date.day)
        
        if today_date==user_data["currentDate"]:
            if user_data['actionAllowd_today']>0:
                if is_login==0:   
                    updated_user_data=user_data
                    del updated_user_data["user_id_mongo"]
                    updated_user_data["actionAllowd_today"] -=1  # reduce one action from allowed
                    updated_user_data["currentDate"]=today_datetime_as_date
                  
                    self.user_db_dal.update_record_db(user_id_mongo, updated_user_data) # update mongoDB
                    self.update_user_json_file(updated_user_data, today_datetime_as_date) # update json file
                    return True
                    
                else: # the login page doesnt need to reduce 1 from the actions
                    return True


            else:
                return False #no actions left

        else:
            self.update_user_data(user_data,today_datetime_as_date, user_id_mongo)
            return self.check_action_left_for_user(user_id,is_login)
   

    def token_verification(self, is_login):
        if request.headers and request.headers.get("x-access-token"):
            token=request.headers.get("x-access-token")
            exist, user_name, user_id=self.verify_token(token)
            if exist:
                action_left=self.check_action_left_for_user(user_id, is_login)
                if action_left:
                    return user_name
                else:
                    return "no actions left"
            else:
                return "not authorized"
        else:
            return "not authorized"

        

    #Check existance of that user in data source and if exists - returns a unique value
    def __check_user(self,username, email):
        users_list= self.users_url_dal.get_users_data()
        for user in users_list:
            if user['username']== username and user['email']== email:
                return user['id']
            
        return None

    
    def get_users_for_file(self):
        users_list=self.user_json_file.get_users_file_data()
        return users_list


    def update_user_json_file(self, updated_user_data, today_datetime_as_date):
        user_file_data=self.get_users_for_file()

        action_record={}
        action_record["id"]=int(updated_user_data["ExternalID"])
        action_record["maxActions"]=int(updated_user_data["maxActions"])
        action_record["date"]=today_datetime_as_date.strftime("%d/%m/%Y")   # string
        action_record["actionAllowd"]=int(updated_user_data["actionAllowd_today"])

        user_file_data["actions"].append(action_record)

        self.user_json_file.update_file_data(user_file_data)
        