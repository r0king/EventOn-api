

from plugins.sheetAccess.sheets import create_google_sheet, get_google_sheet
from fastapi import HTTPException
def get_clean_sheet(user_id,sheet_id,columns_used):
    sheet = get_google_sheet(user_id,sheet_id)
    Data_using = []
    DataMissing = 0

    for rowNum, user in enumerate(sheet):
        userData =[]
        if rowNum == 0:
            Header=user    

        else:

            userData = [col for colNo,col in enumerate(user) if colNo in columns_used and col not in [' ',''] ] 

            if len(userData) == len(columns_used):
                Data_using.append(userData)
            else:
                DataMissing += 1
    return {'Data Missing':DataMissing, "Header":Header, "Data":Data_using}

sheet = get_clean_sheet(user_id='123royalbabu@gmail.com',sheet_id='1Panc38euN3T3szKswT_ycu6kaowKGhklzcCjBiUrmZ4',columns_used=[0,1])

print(sheet)

# for each in sheet['sheets']:
#     for feweach in each['data'][0]['rowData']:
#         print( "{0} {1}".format(feweach['values'][0]['userEnteredValue']['stringValue'],feweach['values'][1]['userEnteredValue']['stringValue']))