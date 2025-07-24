'''Серверная часть Бэкенд СУБД.'''
import json
from flask import Flask, Response, render_template, url_for, request, abort, redirect
import gspread
from google.oauth2.service_account import Credentials
#import database_inter as db

with open("error_list.json", "r",encoding='UTF-8') as error_list:
    error_list = json.load(error_list)

app = Flask(__name__)
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
sheet = client.open_by_key(SPREADSHEET_ID)


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
def error_back(error,problem=0):
    error=error_list[error]
    return render_template('error.html',error=error,problem=problem)


@app.before_request
def check_ip():
    app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  # Запрет доступа к cookie из JS
    SESSION_COOKIE_SECURE=True,     # Только HTTPS
    SESSION_COOKIE_SAMESITE='Lax'   # Защита от CSRF
    )
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        abort(403, description="Ваш IP не разрешен")



@app.route('/home', methods=['GET', 'POST'])
def home():
    print(request)
    if request.method == "POST":
        button1=request.form.get('button')
        print(f"\n\t\t\t\t\tButton has been activate, user moved to {button1}\n")
        match button1:
            case 'test':
                return render_template('home.html')
            case 'resident list':
                return redirect('residents')   
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
    worksheet=sheet.sheet1
    records=worksheet.get_all_records()
    if request.method =='POST':
        room=request.form['комната']
        if room == '':
            return render_template('all_residents.html', resident_list=records,room=room)
        else:
            resident_list=[]
            for i in range(len(records)):
            
                if str(room) == str(records[i]['комната']):
                    #print('sovpalo')
                    user=records[i]
                    resident_list.append(records[i])
            return render_template('all_residents.html', resident_list=resident_list,room=room)
    else:
        return render_template('all_residents.html', resident_list=records)

@app.route('/user')   
@app.route('/user/<user_id>', methods=['POST','GET'])
def user_page(user_id=0):
    if request.method == 'POST':
        print('catch')
    worksheet=sheet.sheet1
    records=worksheet.get_all_records()
    #user_id=request.form['user_id']
    
    user=[]
    list_of_users=[]
    for i in range(len(records)):
        
        if str(user_id) == str(records[i]['user_id']):
            #print('sovpalo')
            user=records[i]
            list_of_users.append(records[i])
        else:
            pass
            #print (f'{user_id} is not in sheet \n')
    #print(records[-1],user,list_of_users,user_id)
    if len(list_of_users)>1:
        error='001'
        return error_back(error,list_of_users)
    else:
        if user==[]:
            error='002'
            return error_back(error)
        else:
            return render_template('user_page.html',user=user)



@app.route('/add')
@app.route('/create_resident_data', methods=['POST', "GET"])
def add_resident():
    worksheet=sheet.sheet1
    data_from_form = request.form
    # Формируем новую строку
    if request.method == 'POST':
        new_people={}
        try:
            print(data_from_form)
            for cell in worksheet.row_values(1):
                
                try :
                    data_from_form[str(cell)]
                    print('ошибка не произошла',cell)
                    info=data_from_form[str(cell)]
                    print(cell,info)
                    new_people[cell]=info
                except:
                    print('произошла ошибка',cell)
            new_people['user_id']=worksheet.get_all_records()[-1]['user_id']+1
            print(new_people)
            dict_to_sheet(worksheet,new_people)                    
        except:
            print('произошла ошибка',cell)
 
        return redirect('/')

    else:
        return (render_template('create_resident.html'))
    
@app.route('/test')
def test_page():
    user=sheet.sheet1.get_all_records()[51]
    return render_template('test_page.html',user=user)
if __name__ == "__main__":
    app.run(debug=True)
    