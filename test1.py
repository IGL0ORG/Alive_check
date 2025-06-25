'''Рабочая область тестирования функций, фич, разработки и обучения.'''
import gspread
from google.oauth2.service_account import Credentials
import time
from gspread_formatting import *
import database_inter as db

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)
db.SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
SPREADSHEET_ID = '1UD0ZqwPg11p4-dGnj84K16eAGtun4NZMfL_SQgkgYzE'
db.sheet = client.open_by_key(db.SPREADSHEET_ID).sheet1
structure=db.sheet.get_all_values()[0]
db.print_data()


db.check=False

# Открытие таблицы

