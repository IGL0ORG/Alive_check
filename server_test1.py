'''Серверная часть Бэкенд СУБД.'''

from flask import Flask, Response, render_template, url_for, request, abort, redirect
import gspread
from google.oauth2.service_account import Credentials
#import database_inter as db


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

def dict_to_sheet(worksheet,data):
    ''' Оправляет данные в таблицу в конкретные ячейки'''
    headers = worksheet.row_values(1)
    # Создаем пустую строку с None по умолчанию
    new_row = [None] * len(headers)
    
    # Заполняем значения в соответствующие столбцы
    for key, value in data.items():
        if key in headers:
            col_index = headers.index(key)  # Индекс столбца (начиная с 0)
            new_row[col_index] = value
    
    # Добавляем строку в конец таблицы
    worksheet.append_row(new_row)


@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        abort(403, description="Ваш IP не разрешен")



@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        button1=request.form.get('button')
        print(f"\n\t\t\t\t\tButton has been activate, user moved to {button1}\n")
        match button1:
            case 'test':
                return render_template('home.html')
            case 'resident list':
                return residents()    
            case 'add resident':
                return render_template('create_resident.html')
    else:
        return render_template('home.html')

@app.route('/')
@app.route('/about', methods=['POST','GET'])
def about():
    
    if request.method == "POST":
        return render_template('home.html')
    else:
        return render_template('about.html')

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return (f'{name} page , \n id:{id}')


@app.route('/residents',methods=['POST','GET'])
def residents():
    records=sheet.get_all_records()
    if request.method == 'POST':
        room=request.form.get('комната')
        return render_template('all_residents.html', resident_list=records,room=room)
    return render_template('all_residents.html', resident_list=records)
    


@app.route('/add')
@app.route('/create_resident_data', methods=['POST', "GET"])
def add_resident():
    data_from_form = request.form
    # Формируем новую строку
    if request.method == 'POST':
        new_people={}
        try:
            print(data_from_form)
            for cell in sheet.row_values(1):
                
                try :
                    data_from_form[str(cell)]
                    print('ошибка не произошла',cell)
                    info=data_from_form[str(cell)]
                    print(cell,info)
                    new_people[cell]=info
                except:
                    print('произошла ошибка',cell)
            print(new_people)
            dict_to_sheet(sheet,new_people)                    
        except:
            print('произошла ошибка',cell)
 
        return redirect('/')

    else:
        return (render_template('create_resident.html'))
    

if __name__ == "__main__":
    app.run(debug=True)
    