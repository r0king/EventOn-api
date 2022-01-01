

from plugins.gmail.mail import create_message, send_mapped_message, send_message
from plugins.sheetAccess.sheets import create_google_sheet, get_google_sheet
from fastapi import HTTPException


# for each in sheet['sheets']:
#     for feweach in each['data'][0]['rowData']:
#         print( "{0} {1}".format(feweach['values'][0]['userEnteredValue']['stringValue'],feweach['values'][1]['userEnteredValue']['stringValue']))
print (send_mapped_message(
    to=[
        'roykngbst@gmail.com',
        '123royalbabu@gmail.com'
        ],
    subject='hey Wasup subjec asdft',
    user_id='therwasanattempt@gmail.com', #registered user
    message="hey sup asdf" ))