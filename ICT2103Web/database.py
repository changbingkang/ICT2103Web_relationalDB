from flask import g
#sqlite3
import sqlite3

def connect_to_database():
    #database name sql
    sql = sqlite3.connect('C:/ICT2103Web/ICT2103Web.db')
    #enter sql in row format
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, 'ICT2103Web_db'):
        g.ICT2103Web_db = connect_to_database()
    return  g.ICT2103Web_db

