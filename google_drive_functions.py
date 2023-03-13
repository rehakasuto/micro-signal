from googleapiclient.discovery import build

from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "configuration.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

cred = None
cred = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = "1C_4CiZppnmo0ysXbns16psHtn8Khe1M4WSPvhE1JTT0"

try:
    service = build('sheets', 'v4', credentials=cred)
except:
    service = build('sheets', 'v4', credentials=cred, discoveryServiceUrl=DISCOVERY_SERVICE_URL)


def get_data_by_email(email):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="alerter!A2:C13").execute()
    rows = result.get('values', [])
    for row in rows:
        for value in row:
            if value == email:
                return row
    return None
