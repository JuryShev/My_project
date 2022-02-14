import json

from flask import Flask, request
from database import FurnitureDtabase
import database


def full_check(json_data, stand_comand:dir, name_db):

    a = request.data
    #j = json.loads(a.decode('utf-8'))
    ch_headline = check_headline(json_data, stand_comand)
    if ch_headline != True:
        return ch_headline

    my_db = FurnitureDtabase(name_db=name_db)
    list_tables = my_db.get_tables()
    ch_table = check_table(json_data, list_tables)
    tables = json_data['tables']
    tables_list = tables.keys()
    if ch_table == False:
        return 'Check table False'

    for name_table in tables_list:
        type_columns = my_db.get_type(name_table)
        data_table = tables[name_table]
        ch_type = check_type(data_table, name_table, type_columns)
        if ch_type != True:
            return 'Type error:' + ch_type
    return 'ok'

def check_headline(data, stand_comand:dict):
    flag_check=True

    if data['comand']!=stand_comand['comand']:
        print(f"command {data['comand']} does not match the execute command")
        return  f"command {data['comand']} does not match the execute command"

    if data['user'] != stand_comand['user']:
        print(f"users {data['user']} does not have permission to perform the operation")
        return f"users {data['user']} does not have permission to perform the operation"

    if data['db_comand'] != stand_comand['db_comand']:
        print(f"command {data['db_comand']} does not allow adding data")
        return f"command {data['db_comand']} does not allow adding data"
    return flag_check

def check_type(data, name_table, type_columns):

    check_flag=True
    for row_table in data:
        for name_column in row_table:
            if not isinstance(row_table[name_column], type_columns[name_column]):
                check_flag = f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}' \
                             f' do not match with the database'

                print(f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}" '
                      f'do not match with the database')
                return check_flag

    return check_flag

def check_table(data, list_tables):
    send_tables=set(data['tables'].keys())
    list_tables=set(list_tables)
    check=send_tables<=list_tables
    return check

app=Flask(__name__)
#db=FurnitureDtabase


#_<int:comand>comand, data
@app.route('/furniture/create_company_<name_db>/', methods=['POST'])
def create_company(name_db):

    stand_comand={'comand': 5000,
                  'user': 'admin',
                  'db_comand':1}
    a=request.data
    j=json.loads(a.decode('utf-8'))
    check_error=full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    my_db=FurnitureDtabase(name_db=name_db)
    ### Отправляться в метод add_row только в конструкции списка множектва (столбец 1, столбец 2)
    ###                                                                     данные 1    данные 2

    list_tables = j['tables']
    for name_table in list_tables:
        my_db.clear_table(name_table)
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.add_row(name_table, tuple(title), tuple(value))
    return 'ok'

@app.route('/furniture_/add_personal', methods=['POST'])
def add_personal(name_db):

    stand_comand={'comand': 2000,
                  'user': 'admin',
                  'db_comand':1}
    a=request.data
    j=json.loads(a.decode('utf-8'))
    check_error = full_check(json_data=j, stand_comand=stand_comand, name_db=name_db)
    if check_error != 'ok':
        return check_error
    my_db = FurnitureDtabase(name_db=name_db)
    list_tables = j['tables']
    for name_table in list_tables:
       # my_db.clear_table(name_table)
        list_rows = list_tables[name_table]
        for row in list_rows:
            title = list(row.keys())
            value = [row[i] for i in title]
            my_db.add_row(name_table, tuple(title), tuple(value))
    return 'ok'

@app.route('/furniture/add_db', methods=['POST'])
def add_factory(comand=1111):

    stand_comand={'comand': comand,
                  'user': '0',
                  'db_comand':1}
    path_cr_db = "mysql_script/create_database.sql"
    path_cr_tb = "mysql_script/create_table_factory.sql"

    a=request.data
    j=json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error
    database.create_database(j['name_db'], path_cr_db)
    database.create_tables_factory(j['name_db'], path_cr_tb)

    return "ok"

@app.route('/furniture/get_inside_struct_<name_db>/', methods=['POST'])
def get_inside_struct(name_db):
    table_list={"tables": {"conf_criterion":[],
                                    "department":   [],
                                    "bonus_koeficient":[],
                                    "posts":[]
                                    }}
    temp_data={}
    stand_comand = {'comand': 1100,
                    'user': 'admin',
                    'db_comand': 1,
                    }
    my_db = FurnitureDtabase(name_db=name_db)
    a=request.data
    j = json.loads(a.decode('utf-8'))
    check_error = check_headline(j, stand_comand)
    if check_error != True:
        return check_error

    for name_table in table_list["tables"]:
        data_table = my_db.get_data_all(name_table)
        column_table = my_db.get_name_column(name_table)
        for h in data_table:
            for i in range(len(h)):
                if type(h[i]) != str:
                    temp_data[column_table[i][0]] = str(h[i])
                else:
                    temp_data[column_table[i][0]] = str(h[i])
            table_list["tables"][name_table].append(temp_data.copy())
        temp_data.clear()
    print("json")
    json_send = json.dumps(table_list)

    return json_send

# list_tables = db.get_tables()
# stand_comand={ 'comand': 1000,
#                 'user': 'admin',
#                 'db_comand': 1}
# if not check_headline(data, stand_comand=stand_comand):
#         raise Exception('Incorrect entry of header keys')
# set_unk_tables=check_table(data, list_tables)
# if  set_unk_tables!=None:
#     raise Exception(f'unknown table named{set_unk_tables}')
#     pass

#     return "get_data_personal"
# @app.route('/personal', methods=['GET'])
# def get_data_personal():
#     return "get_data_personal"
#
# @app.route('/personal', methods=['POST'])
# def add_data_personal():
#
#     return db.add_new_personal(name, adress, number, certification)
#
# @app.route('/personal', methods=['GET'])
# def get_alldata_personal():
#     return "get_data_personal"

"""**********Check value***************"""
# for name_table in list_tables:
#     if '#' in name_table:
#         sep_name, limit = name_table.split('#')
#         count = db.count_row(sep_name)
#         if count >= limit:
#             return 'jj'
#
#     list_rows = list_tables[name_table]
#     for row in list_rows:
#         title = list(row.keys())[0]
#         value = row[title]
#         check_value = my_db.check_value(name_table, title, value)
#         if check_value[-1] == '$':
#             return f'department named {check_value[:-1]} already exists'
#         elif check_value[-1] == '%':
#             return f'department named {check_value[:-1]} already exists'
"""***********************************************"""
if __name__ == '__main__':
#    app.debug=True
    app.run( port=5000)