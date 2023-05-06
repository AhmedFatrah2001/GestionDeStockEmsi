import mysql.connector
from mysql.connector import Error

def connection():
    connection = mysql.connector.connect(host='localhost',
                                         database='gestionDeStock',
                                         user='root',
                                         password='123123')
    return connection
