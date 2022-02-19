import requests

class users_url_data:
    def __init__(self):
        pass

    def get_users_data(self):
        resp=requests.get('https://jsonplaceholder.typicode.com/users')
        return resp.json()
