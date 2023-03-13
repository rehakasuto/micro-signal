from googleapiclient.discovery import build

from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "configuration.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

cred = None
cred = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = "1C_4CiZppnmo0ysXbns16psHtn8Khe1M4WSPvhE1JTT0"

service = build('sheets', 'v4', credentials=cred)


def get_data_by_email(email):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="alerter!A2:C13").execute()
    rows = result.get('values', [])
    for row in rows:
        for value in row:
            if value == email:
                return row
    return None





