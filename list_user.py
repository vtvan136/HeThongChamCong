from numpy import array
import pandas as pd
from class_user import User, Admin, Staff

list_staff = []
list_admin = [] 

def createConnection():
    import sqlite3
    from sqlite3 import Error
    path = "F:\Projects\ChamCong\HeThongChamCong\Data\Data.db"
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def getUser():
    '''
    Hàm trả về 1 array các user đọc từ file excel
    '''
    con = createConnection()
    cur = con.cursor()
    

    con.close()
    
    

def getAdmin(path, list_admin):
    df = pd.read_excel(path, sheet_name="Admin")
    list_id = array(df.loc[:, "ID"])

    for i in range(len(list_id)):
        id = list_id[i]
        name = df.iloc[i, 1]
        position = df.iloc[i, 2]
        password = df.iloc[i, 3]
        admin = Admin(id, name, position, password)
        list_admin.append(admin)

    return list_admin

def getStaff(path, list_staff):
    df = pd.read_excel(path, sheet_name="Staff")
    list_id = array(df.loc[:, "ID"])

    for i in range(len(list_id)):
        id = list_id[i]
        name = df.iloc[i, 1]
        position = df.iloc[i, 2]
        password = df.iloc[i, 3]
        staff = Staff(id, name, position, password)
        list_staff.append(staff)

    return list_staff

getUser()