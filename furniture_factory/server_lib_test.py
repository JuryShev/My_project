from database import FurnitureDtabase

def check_headline(data, stand_comand:dict):
    flag_check=True

    if data['comand']!=stand_comand['comand']:
        print(f"command {data['comand']} does not match the execute command")
        flag_check=False

    if data['user'] != stand_comand['user']:
        print(f"users {data['user']} does not have permission to perform the operation")
        flag_check = False

    if data['db_comand'] != stand_comand['db_comand']:
        print(f"command {data['db_comand']} does not allow adding data")
        flag_check = False




    return flag_check

def check_type(data, name_table, type_columns):

    check_flag=True
    for row_table in data:
        for name_column in row_table:
            if not isinstance(row_table[name_column], type_columns[name_column]):

                check_flag=f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}' \
                           f' do not match with the database'

                print(f'ERROR WRITE:type the data types of the row "{name_column}" to the table "{name_table}" '
                      f'do not match with the database')
                return check_flag

    return check_flag

def check_table(data, list_tables):
    send_tables=set(data['tables'].keys())
    list_tables=set(list_tables)
    check=send_tables-list_tables

    return check




# my_db=FurnitureDtabase()
# list_tables=my_db.get_tables()
#
#
# data = {
#         'comand': 1000,
#         'user': 'admin',
#         'db_comand': 1,
#         'tables': [ {'conf_criterion':[{'title_criterion':'Порядок_1',
#                                         'max_coef': 5,
#                                         'w_coef':0.5},
#                                         {
#                                          'title_criterion':'Порядок_2',
#                                          'max_coef':5,
#                                          'w_coef':  0.25},
#
#                                         {  'title_criterion':'Порядок_3',
#                                             'max_coef': 5,
#                                             'w_coef': 0.1},
#                                         {
#                                             'title_criterion': 'Порядок_4',
#                                             'max_coef': 5,
#                                             'w_coef': 0.1}
#
#                                        ]},
#                     {'department':[{ 'title': [str,'Отдел_1']},
#                                     {'title':  [str,'Отдел_2']},
#                                     { 'title': [str,'Отдел_3']},
#                                     { 'title': [str,'Отдел_4']}]},
#
#                     {'bonus_koeficient':[{'percentage of profits':[int, 2]}]}]}


data2 = {
        "comand": 1000,
        "user": "admin",
        "db_comand": 1,
        "tables": {"conf_criterion":[{"title_criterion":"Порядок_1",
                                        "max_coef": 5,
                                        "w_coef":5},
                                        {
                                         "title_criterion":"Порядок_2",
                                         "max_coef":5,
                                         "w_coef":  0.25},

                                        {  "title_criterion":"Порядок_3",
                                            "max_coef": 5,
                                            "w_coef": 0.1},
                                        {
                                            "title_criterion": "Порядок_4",
                                            "max_coef": 5,
                                            "w_coef": 0.1}

                                       ],
                    "department":   [{ "title": [str,"Отдел_1"]},
                                    {"title":  [str,"Отдел_2"]},
                                    { "title": [str,"Отдел_3"]},
                                    { "title": [str,"Отдел_4"]}],

                    "bonus_koeficient":[{"percentage of profits":[int, 2]}],
                    }}


# check_table(data2, list_tables)
#
#
# tables=data2['tables']
# tables_list=tables.keys()
# my_db.get_tables()
# for name_table in tables_list:
#     type_columns = my_db.get_type(name_table)
#     data_table = tables[name_table]
#     ch=check_type(data_table, name_table, type_columns)

#
# if check_headline(data, stand_comand=stand_comand):
#     pass
#{"types": [str], "title": ["Отдел_1", "Отдел_2", "Отдел_3", "Отдел_4"]}

# conf_criterion=[
#                 ["Порядок_5", 5, 0.5],
#                 ["Порядок_6", 5, 0.25],
#                 ["Порядок_7", 5, 0.1],
#                 ["Порядок_8", 5, 0.1]]
# name_columns=["title_criterion", "max_coef", "w_coef"]
#
# my_db.add_row("conf_criterion", name_columns, conf_criterion )
# print("finish")

data2 = {
        "comand": 1000,
        "user": "admin",
        "db_comand": 1,
        "tables": {"conf_criterion":[{"title_criterion":"p_1",
                                        "max_coef": 5,
                                        "w_coef":5},
                                        {
                                         "title_criterion":"Порядок_2",
                                         "max_coef":5,
                                         "w_coef":  0.25},

                                        {  "title_criterion":"Порядок_3",
                                            "max_coef": 5,
                                            "w_coef": 0.1},
                                        {
                                            "title_criterion": "Порядок_4",
                                            "max_coef": 5,
                                            "w_coef": 0.1}

                                       ],
                   "department": [{"title": "Отдел_1"},
                                  {"title": "Отдел_2"},
                                  {"title": "Отдел_3"},
                                  {"title": "Отдел_4"}],
                    "bonus_koeficient":[{"percentage of profits":2}]
                   }}



import json
json_object = json.dumps(data2, indent = 4)
print('ok')