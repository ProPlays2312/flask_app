#creating basic login and register functions
import pymysql
import random
import datetime

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="database",
  host="mysql-proplays2312-proplays2312-29cf.e.aivencloud.com",
  password="AVNS_IqBDEspbiDiG4ZPB0qf",
  read_timeout=timeout,
  port=26999,
  user="web",
  write_timeout=timeout,
)

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
            raise Exception("UID already exists")
        else:
            continue
    cursor.execute(f"INSERT INTO login (u_name,uid,pass,c_date) VALUES ('{username}',{uid},'{password}','{date}');")
    connection.commit()
    return True
def login(username, password):
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