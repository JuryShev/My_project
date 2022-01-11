import mysql.connector
import io
import database

# with mysql.connector.connect(
#                 host='127.0.0.1',
#                 user='root',
#                 password='1234',
#                 port='3306'
#                 #database='fur_database'
#
#         ) as connection:
#
#     sql_file = open("mysql_script/create_database.sql")
#     sql_as_string = sql_file.read()
#
#
#     mycursor=connection.cursor()
#     mycursor.execute(sql_as_string)
#     #connection.commit()
name_db='cool_company'
path_cr_db="mysql_script/create_database.sql"
path_cr_tb="mysql_script/create_table_factory.sql"

database.create_database( name_db,path_cr_db)
database.create_tables_factory( name_db,path_cr_tb )

print('ok')