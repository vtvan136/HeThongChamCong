import model
import class_user
import SQLite
from datetime import datetime

def signUp(id, name, position, type, password):
    if SQLite.insertUser(id, name, position, type, password) == 1:
        return 1
    else:
        return -1

def getNewID():
    return SQLite.getNewID()

def signInByFace(img):
    id = model.face_match(img)
    if id != -1:
        return id
    else:
        return -1

def signInByID(id, password):
    result = SQLite.signIn(id, password)
    if result == -1:
        print("Wrong ID")
    if result == -2:
        print("Wrong password")
    return result

def getTime():
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    return dt_string

def getDate():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y")
    return dt_string

def removeUser(id):
    if SQLite.delUser(id) == 1:
        return 1
    else:
        print("No exist")
        return -1

def updateUser(id, name, position, type, password):
    user = SQLite.findUser(id)
    flag = 0
    result = 0
    if user.id != id:
        result = -2
    if user.name != name:
        SQLite.updateName(id, name)
        flag+=1
    if user.position != position:
        SQLite.updatePosition(id, position)
        flag+=1
    if user.type != type:
        SQLite.updateType(id, type)
        flag+=1
    if user.password != password:
        SQLite.updatePassword(id, password)
        flag+=1
    if flag == 0:
        #no change
        print("No change")
        result = -1
        return result
    elif flag == -2:
        # cant update ID
        print("Cant update ID")
        return result
    else:
        result = 1
        return result

def prepare_for_facematch():
    resnet = model.load_resnet()
    saved_data = model.load_saved_data()
    return resnet, saved_data

def checkMatch(img, resnet, saved_data):
    result = model.face_match(img, resnet, saved_data)
    if result != -1:
        return result[0]
    else:
        print("Dont match")
        return -1


def getTimeSheet():
    pass



## Test
#signUp(10, "test", "aasd", "admin", "asd")
print(updateUser(1, "Trần Tuấn Khôi", "Team Leader", "Admin", "123"))