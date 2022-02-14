import requests


class ServerConnector():
    def __init__(self, id_user, adress, port):
        self.id_user = id_user
        self.command = 0
        self.db_command = 0
        self.url = f"http://{adress}:{port}"

    def add_db(self, name_db, command, db_command):
        result = requests.post(f"{self.url}/furniture/add_db",
                               json={
                                   "comand": command,
                                   "user": self.id_user,
                                   "db_comand": db_command,
                                   "name_db": name_db})
        return result

    def add_criterion(self, name_db, data_send):
        result = requests.post(f"{self.url}/furniture/create_company_{name_db}/",
                               json=data_send)
        return result

    def get_struct(self, name_db):
        result = requests.post(f"{self.url}/furniture/get_inside_struct_{name_db}/",json={
                                   "comand": 1100,
                                   "user": self.id_user,
                                   "db_comand": 1})
        return result

    def load_data_all(self, name_db, name_table):
        db_cond = f"select * {name_table}"
        command_server = 1100
        json_ = {"comand": command_server,
                 "user": self.id_user,
                 "db_comand": 1,
                 "db_cond":db_cond
                 }
        self.load_data(json_)
        pass

    def load_data_cond(self):
        pass

    def load_data(self, json_request):
        result = requests.post(f"{self.url}/furniture/get_inside_struct/",
                               json=json_request)
        pass
