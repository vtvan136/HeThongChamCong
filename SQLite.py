import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import connect
def createConnection():
    '''
    Hàm lấy connection để kết nối với database được set trong path

    Param: None
    Return: đối tượng connection
    '''
    path = "F:\Projects\ChamCong\HeThongChamCong\Data\Data.db"
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
path = "F:\Projects\ChamCong\HeThongChamCong\Data\Data.db"

def insertUser(id, name, position, type, password):
    '''
    Hàm để thêm user vào trong database được set sẵn ở path trong hàm createConnection

    Param: id, name, position, type, password
    Return: None
    '''
    user = (id, name, position, type, password)
    sql = "INSERT INTO User(ID, NAME, POSITION, TYPE, PASSWORD) VALUES(?,?,?,?,?)"
    con = createConnection()
    cur = con.cursor()
    cur.execute(sql, user)
    if type == "Admin":
        sql = "INSERT INTO Admin(ID, NAME, POSITION) VALUES(?,?,?)"
    else:
        sql = "INSERT INTO Staff(ID, NAME, POSITION) VALUES(?,?,?)"
    user = (id, name, position)
    cur.execute(sql, user)
    print("Insert user")
    con.commit()
    con.close()
        
def getListUser():
    '''
    Hàm trả về 1 list đối tượng User đọc được từ database

    Param: None
    Return: list_user
    '''
    from class_user import User
    list_user = []
    con = createConnection()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM User")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            user = User(row[0], row[1], row[2], row[3], row[4])
            list_user.append(user)
    con.commit()
    con.close()
    print("Getting list user")
    return list_user

def getListAdmin():
    '''
    Hàm trả về 1 list đối tượng Admin đọc được từ database

    Param: None
    Return: list_admin
    '''
    from class_user import Admin
    list_admin = []
    con = createConnection()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Admin")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            admin = Admin(row[0], row[1], row[2])
            list_admin.append(admin)
    con.commit()
    con.close()
    print("Getting list admin")
    return list_admin

def getListStaff():
    '''
    Hàm trả về 1 list đối tượng Staff đọc được từ database

    Param: None
    Return: list_staff
    '''
    from class_user import Staff
    list_staff = []
    con = createConnection()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Staff")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            staff = Staff(row[0], row[1], row[2])
            list_staff.append(staff)
    con.commit()
    con.close()
    print("Getting list staff")
    return list_staff

def findUser(id):
    '''
    Hàm trả về đối tượng User ứng với id truyền vào

    Param: id: int
    Return: Object User
    '''
    from class_user import User
    con = createConnection()
    cur =con.cursor()
    sql = "SELECT * FROM User WHERE id =" + str(id)
    cur.execute(sql)
    row = cur.fetchone()
    if row != None:
        user = User(row[0], row[1], row[2], row[3], row[4])
        con.close()
        return user
    else:
        return -1

def delUser(id):
    '''
    Hàm xóa đối tượng User ra khỏi database được set ở path trong createConnection 

    Param: id: int
    Return: 1 if succesful
    '''
    if findUser(id) != -1:
        type = findUser(id).type
        con = createConnection()
        cur = con.cursor()
        sql = "DELETE FROM User WHERE id=" + str(id)
        cur.execute(sql)
        if type == "Admin":
            sql1 = "DELETE FROM Admin WHERE id = " + str(id)
        else:
            sql1 = "DELETE FROM Staff WHERE id = " + str(id)
        cur.execute(sql1)
        con.commit()
        con.close()
        return 1
    else:
        return -1


def getNewID():
    '''
    Hàm trả về 1 ID mới chưa tồn tại trong database

    Param: None
    Return: id: int
    '''
    list_id = []
    con = createConnection()
    cur = con.cursor()
    sql = "SELECT ID FROM User GROUP BY ID"
    cur.execute(sql)
    while True:
        row = cur.fetchone()
        if row == None:
            break
        list_id.append(int(row[0]))
    result = 1
    while True:
        if result in list_id:
            result+=1
        else:
            con.close()
            return result
    

'''
insertUser("1", "Trần Tuấn Khôi", "Manager", "Admin", "123")
insertUser("2", "Trần Dương Long", "Manager", "Admin", "123")
insertUser("3", "Võ Tấn Văn", "Manager", "Admin", "123")'''

print(getNewID())

