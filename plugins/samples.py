from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = [  
            # 'https://www.googleapis.com/auth/spreadsheets',
            # 'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/drive'
        ]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    spreadsheet_body = {
        "sheets": [
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
                                            "stringValue": "Aosdfg"

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

            },
            {

            }

        ],
        "properties": {
            "title": "Participant Data"

        }

    }

    # service = build('gmail', 'v1', credentials=creds)
    # # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    # print(labels)

    # service = build('sheets', 'v4', credentials=creds)
    # request = service.spreadsheets().get(spreadsheetId='1Hpx_RzCPPLzI5jyD4G430KHM-lWIE8VEbvnUcuYj4MM',includeGridData=False).execute()
    # response = request
    # print(response)

    # service = build('drive', 'v2', credentials=creds)
    # results = service.files().get(fileId='1Hpx_RzCPPLzI5jyD4G430KHM-lWIE8VEbvnUcuYj4MM',).execute()
    # print(results)

    # # # Call the sheets
    # # results = service.users().labels().list(userId='me').execute()
    # # print(results)
    # # labels = results.get('labels', [])

    # # if not labels:
    # #     print('No labels found.')
    # # else:
    # #     print('Labels:')
    # #     for label in labels:
    # #         print(label['name'])


if __name__ == '__main__':
    main()
