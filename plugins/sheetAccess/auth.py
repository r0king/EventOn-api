
import os
from webbrowser import Error
from fastapi.params import Body
from .Google import Create_Service
from typing import Optional
from fastapi import FastAPI,Request


# def find(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return True

def NewSheet(user_id,CLIENT_SECRET_FILE,API_SERVICE_NAME,API_VERSION,SCOPES):

    # try:
    service = ''
    # if not find(f'token_{user_id}_sheets_v4.pickle','./tokens/') :
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES, user_id=user_id)
    

    # except Exception as E:
    #   newspreadsheet = None
    #   return {'Error':E}

    return service
