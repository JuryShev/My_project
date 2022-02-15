import decimal

import mysql.connector
import io
import json
from client_app import ServerConnector
import copy
import database
name_db='novaja_mebel'
temp_data = {}
data_send = {
    "comand": 1110,
    "user": "admin",
    "db_comand": 1,
    "tables": {
               }}

#my_db = database.FurnitureDtabase(name_db=name_db)
server=ServerConnector("admin", "127.0.0.1",5000)
get_json=server.get_struct(name_db=name_db).content
get_json=json.loads(get_json.decode('utf-8'))
get_json_copy=copy.deepcopy(get_json)
############edit##############################################
get_json_copy["tables"]["conf_criterion"][0]["max_coef"]=7
get_json_copy["tables"]["conf_criterion"][0]["title_criterion"]="Новый порядок 1"

get_json_copy["tables"]["conf_criterion"][2]["title_criterion"]="Новый порядок 2 "

get_json_copy["tables"]["department"][1]["title"]="Отдел сна"
get_json_copy["tables"]["department"][2]["title"]="Отдел экспереметов"

##############################################################

for table in get_json["tables"]:
    value_edit_list = []
    value_list_copy=get_json_copy["tables"][table]
    value_list = get_json["tables"][table]
    for v in range(len(value_list)):
        v_keys=list(value_list[v].keys())
        equal=value_list[v]==value_list_copy[v]
        value_edit_dict = {}
        if equal==False:
            value_edit_dict[v_keys[0]]=value_list[v][v_keys[0]]
            for v_key in v_keys:
                v_orig=value_list[v][v_key]
                v_copy=value_list_copy[v][v_key]
                if v_orig!=v_copy:
                    value_edit_dict[v_key]=v_copy
            if len(value_edit_dict.keys())>0:
                value_edit_list.append(value_edit_dict)
                # data_send["tables"][table]=
    if len(value_edit_list)>0:
        data_send["tables"][table]=value_edit_list

#data_send=json.dumps(data_send)
server.edit_table(name_db=name_db, data_send=data_send)
print("ok")

# with mysql.connector.connect(
#                 host='127.0.0.1',
#                 user='root',
#                 password='1234',
#                 port='3306',
#                 database='novaja_mebel'

        # ) as connection:
# table_list = {"tables": {"conf_criterion": [],
#                              "department": [],
#                              "bonus_koeficient": [],
#                              "posts": []
#                              }}
#
# for name_table in table_list["tables"]:
#         data_table=my_db.get_data_all(name_table)
#         column_table=my_db.get_name_column(name_table)
#         for h in data_table:
#             for i in range(len(h)):
#                 if type(h[i]) != str:
#                     temp_data[column_table[i][0]]= str(h[i])
#                 else:
#                     temp_data[column_table[i][0]]= str(h[i])
#             table_list["tables"][name_table].append(temp_data.copy())
#         temp_data.clear()
# print("json")
# j=json.dumps(table_list)

    # data_send={}
    # mycursor = connection.cursor()
    # mysql_comand_col = 'SHOW COLUMNS from ' + 'conf_criterion'
    # mysql_comand_data = 'SELECT * from ' + 'conf_criterion'
    # mycursor.execute(mysql_comand_col)
    # col=mycursor.fetchall()
    # mycursor.execute(mysql_comand_data)
    # data = mycursor.fetchall()
    # for h in data:
    #     for i in range(len(h)):
    #         if type(h[i])!=str:
    #             data_send[col[i][0]]=str(h[i])
    #         else :
    #             data_send[col[i][0]] = h[i]
    #         print(type(h[i]))



#
#     sql_file = open("mysql_script/create_database.sql")
#     sql_as_string = sql_file.read()
#
#
#     mycursor=connection.cursor()
#     mycursor.execute(sql_as_string)
#     #connection.commit()
# name_db='cool_company'
# path_cr_db="mysql_script/create_database.sql"
# path_cr_tb="mysql_script/create_table_factory.sql"
#
# database.create_database( name_db,path_cr_db)
# database.create_tables_factory( name_db,path_cr_tb )

print('ok')