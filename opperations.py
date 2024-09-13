#Description: This file contains the functions to register and login a user, and to get user data.
# Required Libraries
import pymysql
import random
import datetime
import os
from dotenv import load_dotenv
load_dotenv(".env")
timeout = 10
# Database Connection
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db= os.getenv("DB_NAME"),
  host= os.getenv("DB_HOST"),
  password=os.getenv("DB_PASS"),
  read_timeout=timeout,
  port=(int(os.getenv("DB_PORT"))),
  user=os.getenv("DB_USER"),
  write_timeout=timeout,
)
# Function to get user data
def data(uid):
    #fetch data from database
    cursor = connection.cursor()
    cursor.execute(f"SELECT login.c_date, data.name, data.email, data.quote FROM login INNER JOIN data ON login.u_name = data.u_name WHERE login.uid = {uid};")
    a = cursor.fetchall()
    connection.commit()
    return a[0]["c_date"], a[0]["name"], a[0]["email"], a[0]["quote"]
# Function to check for SQL Injection
def check_sqli(input_string):
    # SQL Injection payloads
    sqli_payloads = ["'", "\"", ";", "--", "/*", "*/", "xp_", "exec", "sp_", "xp_cmdshell", "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "JOIN", "WHERE", "FROM", "UNION", "HAVING", "ORDER", "GROUP", "BY", "COUNT", "INTO", "VALUES", "DECLARE", "SET", "TRUNCATE", "REPLACE", "FETCH", "SUBSTRING", "CONVERT", "CAST", "HAVING", "EXISTS", "BETWEEN", "LIKE", "IN", "IS", "NULL", "AND", "OR", "NOT", "ALL", "ANY", "SOME", "CASE", "WHEN", "THEN", "ELSE", "END", "AS", "ASC", "DESC", "LIMIT", "OFFSET", "INNER", "OUTER", "LEFT", "RIGHT", "FULL", "CROSS", "NATURAL", "JOIN", "ON", "USING", "WHEN", "MATCH", "AGAINST", "LIKE", "REGEXP"]
    # Check for SQL Injection
    for i in sqli_payloads:
        if i in input_string:
            raise Exception("SQL Injection detected")
    return True
# Function to register a user
def register(username, password, name, email, quote):
    #check for SQL Injection
    try:
        if check_sqli(username) or check_sqli(password) or check_sqli(name) or check_sqli(email) or check_sqli(quote):
            pass
    except Exception as e:
        raise e
    uid = random.randint(10000,99999) ^ 12345
    date = datetime.date.today().strftime("%Y-%m-%d")
    cursor = connection.cursor()
    cursor.execute(f"SELECT u_name,uid FROM login;")
    a = cursor.fetchall()
    #check if username or uid already exists
    for i in a:
        if i["u_name"] == username:
            raise Exception("Username already exists")
        else:
            continue
    #check if uid already exists
    for i in a:
        if i["uid"] == uid:
            return register(username, password)
        else:
            continue
    #insert data into database
    cursor.execute(f"INSERT INTO login (u_name,uid,pass,c_date) VALUES ('{username}',{uid},'{password}','{date}');")
    cursor.execute(f"INSERT INTO data (u_name,name,email,quote) VALUES ('{username}','{name}','{email}','{quote}');")
    connection.commit()
    return True
# Function to login a user
def login(username, password):
    #check for SQL Injection
    try:
        if check_sqli(username) or check_sqli(password):
            pass
    except Exception as e:
        raise e
    #check if username exists
    cursor = connection.cursor()
    cursor.execute(f"SELECT u_name FROM login;")
    a = cursor.fetchall()
    try:
        if not any(username in i.values() for i in a):
            raise Exception("Username not found")
    except Exception as e:
        raise e
    #check if password is correct
    cursor.execute(f"SELECT uid FROM login WHERE u_name = '{username}' AND pass = '{password}';")
    a = cursor.fetchall()
    try:
        if not a:
            raise Exception("Incorrect password")
        else:
            date, name, email, quote = data(a[0]["uid"])
            return(date, name, email, quote)
    except Exception as e:
        raise e
