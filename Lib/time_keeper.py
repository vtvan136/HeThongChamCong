import os
import shutil
import datetime
from openpyxl import workbook
import pandas as pd
import openpyxl
from openpyxl.styles import Border, Side, Alignment
import SQLite 

'''
File chứa các hàm dùng để xử lý dữ liệu việc chấm công
Mô tả chung:
    - Folder chính là TimeKeeper
    - Các folder con được đặt tên theo tháng
    - Trong các folder con là các file excel là báo cáo chấm công từng người
Ý tưởng:
    - Các file báo cáo chấm công được clone từ 1 file gốc (form.xlsx)
    - Tạo folder các tháng (kiểm tra tồn tại)
    - Tạo file chấm công theo id của từng folder (kiểm tra tồn tại)
    - 
'''

TIME_IN = int(8) # giờ vào ca
TIME_OUT = int(17) # giờ tan ca

def getDate():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y")
    return dt_string.split("/")[0]

def getMonth():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y")
    return dt_string.split("/")[1]

def getHour():
    return datetime.datetime.now().hour

def getMinute():
    return datetime.datetime.now().minute

def checkExistDirectory(month):
    '''
    Hàm kiểm tra xem folder của tháng hiện nay đã tồn tại chưa

    Param: month
    Return: True nếu đã tồn tại và ngược lại
    '''
    lst_dir = os.listdir("TimeKeeper")
    if str(month) in lst_dir:
        return True
    else:
        return False

def createMonthDirectory(month):
    '''
    Hàm tạo folder của tháng hiện nay

    Param: month
    Return: 1 nếu thành công, -1 nếu đã tồn tại
    '''
    if checkExistDirectory(month) == False:
        os.mkdir("TimeKeeper/" + month)
        return 1
    else:
        return -1

def checkExistTimeSheet(id, month):
    '''
    Hàm kiểm tra xem đã tồn tại file chấm công của id chưa

    Param: id, month
    Return: True nếu đã tồn tại và ngược lại
    '''
    path = "TimeKeeper/" + str(month)
    lst = os.listdir(path)
    if str(id) + ".xlsx" in lst:
        return True
    else:
        return False

def createTimeSheet(id, month):
    '''
    Hàm tạo file chấm công mới của id dựa trên Form.xlsx

    Param: id, month
    Return: 1 nếu thành công, -1 nếu đã tồn tại
    '''
    path = "TimeKeeper/" + str(month) + "/" + str(id) + ".xlsx"
    if checkExistTimeSheet(id, month) == False:
        shutil.copy2("TimeKeeper\Form.xlsx" , path)
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        sheet['E2'] = month
        user = SQLite.findUser(id)
        sheet['A3'] = "ID: " + str(user.id)
        sheet['B3'] = "Tên: " + user.name
        sheet['F3'] = "Vị trí: " + user.position

        day = datetime.date(2021, int(month), 1) #first day
        sheet['A6'] = str(day)

        for i in range(7,38):
            address = "A" + str(i)
            day += datetime.timedelta(days = 1)
            if day.strftime("%m") != month:
                break
            sheet[address] = str(day)

        workbook.save(path)
        return 1
    else:   
        return -1

def getAddressOfDate(day):
    '''
    Hàm trả về vị trí cell của ngày hiện tại trong file

    Param: day
    Return: Vị trí của cell (Vd: A27), -1 nếu không thành công
    ''' 
    return str(int(day) + 5)

def checkAllTimeSheet(month, list_id):
    '''
    Hàm kiểm tra xem đã đầy đủ hết các timesheets chưa

    Param: month
    Return: True nếu đủ và ngược lại
    '''
    path = "TimeKeeper/" + str(month)
    list_file = os.listdir(path)
    for id in list_id:
        if str(id) + ".xlsx" not in list_file:
            return False
    return True

def check(month):
    '''
    Hàm kiểm tra tất cả (bao gồm folder và các timesheets), nếu chưa thì tạo mới

    Param: month
    Result: True 
    '''
    # check folder của tháng
    if checkExistDirectory(month) == False:
        createMonthDirectory(month)
    # check all Timesheets
    list_id = SQLite.getListID()
    for id in list_id:  
        if checkExistTimeSheet(id, month):
            continue
        else:
            createTimeSheet(id, month)
    
def loader():
    ''''
    Hàm load các biến cần thiết để tối ưu thời gian
    
    Return: day, month, list_id
    '''
    month = getMonth()
    day = getDate()
    list_id = SQLite.getListID()
    check(month)
    return month, day, list_id

def calculate(out, hour, minute):
    '''
    Hàm tính toán thời gian trễ giờ hoặc tăng ca

    Param:
        out: nếu = 0 thì là check in, = 1 thì là check out
        hour: giờ thực tế
        minute: phút thực tế
    Return: thời gian chênh lệch 
    '''
    if out == 0:
        temp = TIME_IN * 60
    else:
        temp = TIME_OUT * 60
    delta = int(hour)*60 + int(minute) - int(temp)
    return str(delta // 60) + ":" + str(delta % 60)
    
def timeKeeping(id, month, day):
    '''
    Hàm dùng để chấm công, lưu thời gian vào TimeSheet

    Param: id, month, day
    Return: 
    '''
    path = "TimeKeeper/" + str(month) + "/" + str(id) + ".xlsx" 
    out = 0 # Mặc định là check in, nếu check out thì out = 1

    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    address = "B" + str(getAddressOfDate(day))
    address1 = "D" + str(getAddressOfDate(day))
    cell = sheet[address].value
    if cell != None:
        out = 1
        address = "C" + str(getAddressOfDate(day))
        address1 = "E" + str(getAddressOfDate(day))
    time = str(getHour()) + " : " + str(getMinute())
    sheet[address] = time
    delta = calculate(out, getHour(), getMinute()) #Tính thời gian chênh lệch
    sheet[address1] = delta
    workbook.save(path)

if __name__ == "__main__":    
    month, day, list_id = loader()
    check(month)
    timeKeeping(1, month, day)
    