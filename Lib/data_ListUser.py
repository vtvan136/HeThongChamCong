import xlsxwriter
import os
from list_user import *



def checkExist():
    path = "F:\Projects\ChamCong\HeThongChamCong\Data"
    if os.path.isfile("ListUser.xls"):
        return True
    else:
        return False

def CreatFile():
    #User
    pass



