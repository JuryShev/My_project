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
data_send_2= {
    "comand": 5000,
    "user": "admin",
    "db_comand": 1,
    "tables": {
               }}
answer_server='none_operation'
flag_add_del_edit=''

#my_db = database.FurnitureDtabase(name_db=name_db)
server=ServerConnector("admin", "127.0.0.1",5000)
server.name_db=name_db

import sys
get_json=server.get_struct(name_db=name_db).content
get_json = json.loads(get_json.decode('utf-8'))

# data_send_2['tables']=get_json['tables']
# server.add_criterion(name_db=name_db, data_send=data_send_2)
get_json_copy=copy.deepcopy(get_json)
############edit##############################################
get_json_copy["tables"]["conf_criterion"][0]["max_coef"]=7
get_json_copy["tables"]["conf_criterion"][0]["title_criterion"]="Новый порядок 1"

get_json_copy["tables"]["conf_criterion"][2]["title_criterion"]="Новый порядок 2 "

get_json_copy["tables"]["department"][1]["title"]="Отдел сна"
get_json_copy["tables"]["department"][2]["title"]="Отдел экспереметов"

####симуляция удаления строки#########################################
# get_json_copy["tables"]["conf_criterion"].pop(3)
# get_json_copy["tables"]["conf_criterion"].pop(3)
# get_json_copy["tables"]["department"].pop(3)
# get_json_copy["tables"]["department"].pop(3)
##########################################################################
####симуляция добавления строки#########################################
get_json_copy["tables"]["conf_criterion"].append({"title_criterion":"Добавленный критерий_4",
                                        "max_coef": 5,
                                        "w_coef":5.0})
get_json_copy["tables"]["department"].append({"title":  "Отдел_13"})

get_json_copy["tables"]["conf_criterion"].append({"title_criterion":"Добавленный критерий_5",
                                        "max_coef": 5,
                                        "w_coef":5.0})
get_json_copy["tables"]["department"].append({"title":  "Отдел_отдыха"})
#########################################################################
##############################################################
#### del row ##########################################
# добавили count_del_row строк в конец таблицы
# отправляем индекс строки на удаления
# вызвать функцию удаления строк
for table in get_json["tables"]:
    id_dict={}
    id_list=[]
    value_list_copy = get_json_copy["tables"][table]
    value_list = get_json["tables"][table]
    count_del_row = len(value_list) - len(value_list_copy)
    if count_del_row > 0:
        value_list = get_json["tables"][table][-count_del_row:]
        id_key=list(value_list[0].keys())[0]
        for value_dict in value_list:
            id_dict[id_key]=value_dict[id_key]
            id_list.append(id_dict.copy())
            pass
            # id_dict.append({[v_keys[0]]:value_dict[v_keys[0]})### id-должен быть лист с добавленнием словаря через dict [v_keys[0]]=value_dict[v_keys[0]]
        data_send["tables"][table] = id_list
if len(data_send["tables"])>0:
    answer_server=server.del_row_table(data_send=data_send).content.decode("utf-8")
    data_send["tables"].clear()
    print(answer_server)
    if answer_server == 'ok':
        get_json = server.get_struct(name_db=name_db).content# загрузка обновленых таблиц
        get_json = json.loads(get_json.decode('utf-8'))
######################################################################

###############add row #####################################################
if answer_server=='ok' or answer_server=='none_operation':
    save_count_add_row={}
    for table in get_json["tables"]:
        value_add_list = []
        value_list_copy = get_json_copy["tables"][table]
        value_list = get_json["tables"][table]
        count_add_row = len(value_list) - len(value_list_copy)
        save_count_add_row[table]=abs(count_add_row)
        if count_add_row<0:
            value_list_copy=get_json_copy["tables"][table][-abs(count_add_row):]
            data_send["tables"][table]=value_list_copy
    if len(data_send["tables"])>0:
        answer_server=server.add_row_table(data_send=data_send).content.decode("utf-8")
        data_send["tables"].clear()
        print(answer_server)
        if answer_server == 'ok':
            get_json = server.get_struct(name_db=name_db).content  # загрузка обновленых таблиц
            get_json = json.loads(get_json.decode('utf-8'))
            for table in get_json["tables"]:
                value_list = get_json["tables"][table]
                value_list_copy=get_json_copy["tables"][table].copy()
                count_add_row=save_count_add_row[table]
                if count_add_row>0:
                    value_list_copy[-count_add_row:]=value_list[-count_add_row:]
                    get_json_copy["tables"][table].clear()
                    get_json_copy["tables"][table]= value_list_copy

#############################################################

###############edit row#####################################################
if answer_server=='ok' or answer_server=='none_operation':
    for table in get_json["tables"]:
        value_edit_list = []
        value_list_copy=get_json_copy["tables"][table]
        value_list = get_json["tables"][table]

        for v in range(len(value_list)):
            v_keys=list(value_list[v].keys())
            equal=value_list[v]==value_list_copy[v]# проверка на редактирование
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