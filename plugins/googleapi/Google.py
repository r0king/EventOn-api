import datetime
import pickle
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes ,user_id):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None
    tokenfile = f'plugins/sheetAccess/tokens/token_{user_id}_{API_SERVICE_NAME}_{API_VERSION}.json'
    # print(pickle_file)

    if os.path.exists(tokenfile):
        with open(tokenfile, 'rb') as token:
            cred = Credentials.from_authorized_user_file(tokenfile, SCOPES)

    if not cred or not cred.valid:
        # if cred and cred.expired and cred.refresh_token:
        #     # cred.refresh(Request())
        #     refreshing expired token not working
        # else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        cred = flow.run_local_server(success_message='The Authentication Was succssfull You May Now Close This Window ',port=8080)

        with open(tokenfile, 'w') as token:
            token.write(cred.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt