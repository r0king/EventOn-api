

from plugins.sheetAccess.sheets import create_google_sheet, get_google_sheet
from fastapi import HTTPException

sheet = get_google_sheet('123royalbabu@gmail.com','1Panc38euN3T3szKswT_ycu6kaowKGhklzcCjBiUrmZ4')
columns_used = [0,2]
Data_using = []

for rowNum, user in enumerate(sheet):
    userData =[]
    if rowNum == 0:
        Header=user    

    else:

        userData = [col for colNo,col in enumerate(user) if colNo in columns_used and col != ' '] 
        if len(userData) == len(columns_used):
            Data_using.append(userData)

print(Header,Data_using)


# for each in sheet['sheets']:
#     for feweach in each['data'][0]['rowData']:
#         print( "{0} {1}".format(feweach['values'][0]['userEnteredValue']['stringValue'],feweach['values'][1]['userEnteredValue']['stringValue']))