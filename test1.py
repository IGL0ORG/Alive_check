import gspread
from google.oauth2.service_account import Credentials

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1
data=sheet.get_all_cells()
print(data)