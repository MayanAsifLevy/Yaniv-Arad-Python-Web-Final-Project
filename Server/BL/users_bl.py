from Server.DAL.user_DB_DAL import Mongo_users_DB



class Users:
    def __init__(self):
        self.users_DB_dal=Mongo_users_DB()
        

    # users from mongoDB
    def get_users_data(self):
        users_list=self.users_DB_dal.get_user_tbl()
        return users_list
        
