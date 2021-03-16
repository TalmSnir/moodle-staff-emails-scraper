
from oauth2client.service_account import ServiceAccountCredentials
import gspread


SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# pay attension that your credentials file will be named credentials.json or change the path in the script
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', SCOPES)

# !change 'your sheet name' to the google drive sheet's name
client = gspread.authorize(creds)
sheet = client.open('your sheet name').sheet1


def write_to_sheet(name, email):
    sheet.insert_row([name, email])
