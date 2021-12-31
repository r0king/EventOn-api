 
from plugins.googleapi.auth import NewSheet
# from googleapi.auth import NewSheet



def create_google_sheet(user_id,sheet_name='Student'):

    CLIENT_SECRET_FILE = 'plugins/googleapi/Credentials/keys.json'
   API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    sheet_body = {
          'properties': {
              'title': f'{sheet_name}',
              'locale': 'en_US', # optional
              'autoRecalc': 'ON_CHANGE', # calculation setting #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#RecalculationInterval
              }
          ,
          'sheets': [
            {
                "data": [
                    {
                        "rowData": [
                            {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Name"
                                                               
                                        }

                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Mail"

                                        }

                                    }

                                ]
                            }

                        ]

                    }

                ],
                "properties": {
                    "title": "Data"

                }

            }
          ]
      }
    service = NewSheet(user_id=user_id,CLIENT_SECRET_FILE=CLIENT_SECRET_FILE,API_SERVICE_NAME=API_SERVICE_NAME,API_VERSION=API_VERSION,SCOPES=SCOPES)
    newspreadsheet = service.spreadsheets().create(body=sheet_body).execute()
    return newspreadsheet

def get_google_sheet(user_id,sheetid):
    CLIENT_SECRET_FILE = 'plugins/googleapi/Credentials/keys.json'
    API_SERVICE_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    service = NewSheet(user_id=user_id,CLIENT_SECRET_FILE=CLIENT_SECRET_FILE,API_SERVICE_NAME=API_SERVICE_NAME,API_VERSION=API_VERSION,SCOPES=SCOPES)
    sheet = service.spreadsheets().values().get(spreadsheetId=sheetid,range='A:Z').execute()
    return sheet['values']

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
