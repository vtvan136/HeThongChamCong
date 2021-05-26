class User:
    def __init__(self, id = None, name = None, position = None, type = None, password = None):
        self.id = id
        self.name = name 
        self.position = position
        self.type = type
        self.password = password
    
    def timeKeeping(self, time):
        '''
        Phương thức để chấm công, bổ sung sau vì chưa hình dung được quá trình
        Input: thời gian chấm công (id)
        '''
        pass
    def signIn(self, id, password):
        from SQLite import signIn
        return signIn(id, password)


class Staff(User):

    def __init__(self, id, name, position):
        super().__init__(id=id, name=name, position=position)
        self.type = "Staff"



class Admin(User):

    def __init__(self, id, name, position):
        super().__init__(id=id, name=name, position=position)
        self.type = "Admin"    

    def getNewUser(self, id, name, position, type, password):
        from SQLite import insertUser
        if insertUser(id, name, position, type, password):
            return 1
        else:
            return -1
    
    def findUser(self, id):
        from SQLite import findUser
        if findUser(id) != -1:
            return findUser(id)
        else:
            return -1
    
    def delUser(self, id):
        from SQLite import delUser
        if delUser(id) != -1:
            return 1
        else:
            return -1

    def getNewID(self):
        from SQLite import getNewID
        return getNewID()

    def insertUser(self, id, name, position, type, password):
        from SQLite import insertUser
        return insertUser(id, name, position, type, password)