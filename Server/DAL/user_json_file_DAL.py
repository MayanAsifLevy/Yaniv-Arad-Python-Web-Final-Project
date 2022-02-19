import json
import os

class UsersFile():
    def __init__ (self):
        pass

    def get_users_file_data(self):

        path = os.path.join(os.getcwd(),"Server\Data\Actions.json")
        with open (path, 'r') as user_file:
            data=json.load(user_file)
        return data

    def update_file_data(self,user_file_data):
        path = os.path.join(os.getcwd(),"Server\Data\Actions.json")
        with open (path, 'w') as user_file:
            data=json.dump(user_file_data, user_file)

        
            