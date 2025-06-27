'''Рабочая область тестирования функций, фич, разработки и обучения.'''
import gspread
from google.oauth2.service_account import Credentials
import time
from gspread_formatting import *
import database_inter as db
from flask import Flask, render_template, url_for,Response, request, abort, redirect



app = Flask(__name__)
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
sheet = client.open_by_key(SPREADSHEET_ID).worksheet('Лист1')


people=[{'ФИО':'СТепка','user_id':1,'комната':620, 'row':1},{'ФИО':'Алгег','user_id':3,'комната':617,'row':2},{'ФИО':'Русланчик','user_id':2,'комната':617,'row':3}]
filters={'комната':617}
for row in people:
        
        #try: 
        for filter in list(filters.keys()): # прохождение по запрашиваемым фильтрам
            if str(row[filter]) != str(filters[filter]):
                #print(row)
                del people[row['row']]
people.append('\t\t')
#print(people)

@app.route('/s')
@app.route('/create_resident')
def create_resident():
    return render_template('create_resident.html')


@app.route('/add')
@app.route('/create_resident_data', methods=['POST', "GET"])
def add_resident():
    data_from_form = request.form
    # Формируем новую строку
    if request.method == 'POST':
        new_people={}
        try:
            for cell in sheet.row_values(1):
                for i in range(len(data_from_form)):
                    print(data_from_form[str(cell)])
                    
                    info=data_from_form[str(cell)]
                    print(cell,info)
                    new_people[cell]=info

                    print(new_people)
        except:
            print('произошла ошибка',cell)

            
            # Добавляем в конец таблицы
        sheet.append_row(new_people)
        return redirect('/')

    else:
        return (render_template('create_resident.html'))
@app.route('/')
def testing():
    records = sheet.get_all_records()
    
    # Форматируем как текст с переносами
    text_response = "\n".join(str(record) for record in records)
    return Response(text_response, mimetype='text/plain')


if __name__ == "__main__":
    app.run(debug=True)
# Открытие таблицы

