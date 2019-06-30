import pickle
import os.path
import sys
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    if (sys.stdin.isatty() == False):
        export_data = sys.stdin.read()
    else:
        if (len(sys.argv) == 2):
            try:
                export_data = open(sys.argv[1]).read()
            except:
                print('Error: make sure to provide a valid file')
                sys.exit()
        else:
            print('Error: please provide a single file at a time')
            sys.exit()

    print('Authenticating...')

    creds = None
    if os.path.exists(str(Path.home()) + '/.sheetimportrc'):
        with open(str(Path.home()) + '/.sheetimportrc', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open(str(Path.home()) + '/.sheetimportrc', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    spreadsheet = {
        'properties': {
            'title': 'Data imported by sheetimport'
        },
        'sheets': {
            'properties': {
                'title': 'data'
            },
        },
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()

    print('Creating spreadsheet...')

    spreadsheet_id = spreadsheet.get('spreadsheetId')

    sheet_id = service.spreadsheets().get(spreadsheetId = spreadsheet_id, includeGridData = True).execute()['sheets'][0]['properties']['sheetId']

    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = { 'requests': [
            { 'pasteData': {
                'coordinate': {
                    'sheetId': sheet_id,
                    'rowIndex': 0,
                    'columnIndex': 0
                },
                'data': export_data,
                'delimiter': ',',
                } }
            ] }
    ).execute()

    print('https://docs.google.com/spreadsheets/d/{0}/edit'.format(spreadsheet.get('spreadsheetId')))

if __name__ == '__main__':
    main()
