from flask import Flask, render_template, url_for, request, abort, redirect
import gspread
from google.oauth2.service_account import Credentials


app = Flask(__name__)
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


ALLOWED_IPS = [
        '127.0.0.1'
]

@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        abort(403, description="Ваш IP не разрешен")


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return (f'{name} page , \n id:{id}')


@app.route('/residents')
def residents():
    # Получаем все данные
    residents = sheet.get_all_records()
    for user in len(residents):
        return {residents}



@app.route('/add', methods=['POST', "GET"])
def add_resident():
    data = request.form
    # Формируем новую строку
    if request.method == 'POST':
        new_row = [
            data['id'],
            data['name'],
            data['room'],
            data['phone'],
            data['check_in_date']
        ]
        # Добавляем в конец таблицы
        sheet.append_row(new_row)
    else:
        return (render_template('create_resident.html'))


@app.route('/s')
def testing():
    return sheet.get("A1:D4")



if __name__ == "__main__":
    app.run(debug=True)
    