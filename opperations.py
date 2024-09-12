#creating basic login and register functions
import pymysql
import random
import datetime
import os
from dotenv import load_dotenv
load_dotenv(".env")
timeout = 10
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
# Function to check for SQL Injection
def check_sqli(input_string):
    sqli_payloads = ["'", "\"", ";", "--", "/*", "*/", "xp_", "exec", "sp_", "xp_cmdshell", "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "JOIN", "WHERE", "FROM", "UNION", "HAVING", "ORDER", "GROUP", "BY", "COUNT", "INTO", "VALUES", "DECLARE", "SET", "TRUNCATE", "REPLACE", "FETCH", "SUBSTRING", "CONVERT", "CAST", "HAVING", "EXISTS", "BETWEEN", "LIKE", "IN", "IS", "NULL", "AND", "OR", "NOT", "ALL", "ANY", "SOME", "CASE", "WHEN", "THEN", "ELSE", "END", "AS", "ASC", "DESC", "LIMIT", "OFFSET", "INNER", "OUTER", "LEFT", "RIGHT", "FULL", "CROSS", "NATURAL", "JOIN", "ON", "USING", "WHEN", "MATCH", "AGAINST", "LIKE", "REGEXP"]
    for i in sqli_payloads:
        if i in input_string:
            raise Exception("SQL Injection detected")
    return True
# Function to register a user
def register(username, password):
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
    for i in a:
        if i["uid"] == uid:
            return register(username, password)
        else:
            continue
    cursor.execute(f"INSERT INTO login (u_name,uid,pass,c_date) VALUES ('{username}',{uid},'{password}','{date}');")
    connection.commit()
    return True
# Function to login a user
def login(username, password):
    try:
        if check_sqli(username) or check_sqli(password):
            pass
    except Exception as e:
        raise e
    cursor = connection.cursor()
    cursor.execute(f"SELECT u_name,pass FROM login;")
    a = cursor.fetchall()
    for i in a:
        if i["u_name"] == username:
            if i["pass"] == password:
                print("Login successful")
                return True
            else:
                raise Exception("Incorrect password")
        else:
            raise Exception("Username not found")
    return False
