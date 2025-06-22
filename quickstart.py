import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request

app = Flask(__name__)

# Авторизация
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1-zpOWgJd32cwLBDa9Wt14HkuBxJmVvTbY2aaXRw18dA'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

@app.route('/add', methods=['POST'])
def add_resident():
    data = request.form
    # Формируем новую строку
    new_row = [
        data['id'],
        data['name'],
        data['room'],
        data['phone'],
        data['check_in_date']
    ]
    # Добавляем в конец таблицы
    sheet.append_row(new_row)
    return "Жилец добавлен!"

@app.route('/')
@app.route('/residents')
def get_residents():
    # Получаем все данные
    residents = sheet.get_all_records()
    return {'residents': residents}

if __name__ == '__main__':
    app.run(debug=True)