
import os
from webbrowser import Error
from fastapi.params import Body
from Google import Create_Service
from typing import Optional
from fastapi import FastAPI,Request

CLIENT_SECRET_FILE = './keys.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


# def find(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return True

def create_sheet(user_id):
    sheet_body = {
          'properties': {
              'title': 'Student List',
              'locale': 'en_US', # optional
              'autoRecalc': 'ON_CHANGE', # calculation setting #https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#RecalculationInterval
              }
          ,
          'sheets': [
              {
                  'properties': {
                      'title': 'Certificate'
                  }
              }
          ]
      }
    try:
      service = ''
      # if not find(f'token_{user_id}_sheets_v4.pickle','./tokens/') :
      service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES, user_id=user_id)
      newspreadsheet = service.spreadsheets().create(body=sheet_body).execute()

    except Exception as E:
      newspreadsheet = None
      return {'Error':E}

    return newspreadsheet
