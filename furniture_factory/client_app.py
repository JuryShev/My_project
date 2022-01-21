import requests
class ServerConnector():
    def __init__(self, id_user, adress, port):
        self.id_user=id_user
        self.comand=0
        self.db_comand=0
        self.url=f"http://{adress}:{port}"

    def add_db(self, name_db, comand, db_comand):
        result=requests.post(f"{self.url}/futniture/add_db",
                             json={
                        "comand": comand,
                        "user": self.id_user,
                        "db_comand": db_comand,
                        "name_db": name_db})

        return result

    def add_criterion(self, name_db,  data_send):
        result = requests.post(f"{self.url}/futniture/create_company_{name_db}/",
                               json=data_send)

        return result



