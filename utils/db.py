import mysql.connector as mysql_connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

def get_connection():
    load_dotenv()
    mysql_host = os.getenv('mysql_host')
    mysql_database = os.getenv('mysql_database')
    mysql_user = os.getenv('mysql_user')
    mysql_password = os.getenv('mysql_password')
    try:
        db_connection = mysql_connector.connect(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password, use_pure=True)
    except mysql_connector.Error as e:
        if e.errno==errorcode.ER_BAD_DB_ERROR:
            with mysql_connector.connect(host=mysql_host, user=mysql_user, password=mysql_password, use_pure=True) as con:
                with con.cursor() as cursor:
                    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {mysql_database}')
                    con.commit()
                    db_connection = mysql_connector.connect(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password, use_pure=True)
            
    return db_connection

def init_tables():
    db_connection = get_connection()
    cursor = db_connection.cursor()
    for db_file in os.scandir('./ddl_tables'):
        with open(db_file.path) as sql_file:
            cursor.execute(sql_file.read())
            db_connection.commit()
    db_connection.close()




