'''Рабочая область тестирования функций, фич, разработки и обучения.'''
import gspread
from google.oauth2.service_account import Credentials
import time
from gspread_formatting import *
#import database_inter as db
from flask import Flask, render_template, url_for,Response, request, abort, redirect



app = Flask(__name__)
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)

# Открытие таблицы
SPREADSHEET_ID = '1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
sheet = client.open_by_key(SPREADSHEET_ID).worksheet('Лист1')
#sheet=client.open_by_url('https://docs.google.com/spreadsheets/d/1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA/edit?gid=0#gid=0').worksheet('Лист1')

#people=[{'ФИО':'СТепка','user_id':1,'комната':620, 'row':1},{'ФИО':'Алгег','user_id':3,'комната':617,'row':2},{'ФИО':'Русланчик','user_id':2,'комната':617,'row':3}]
#filters={'комната':617}
#for row in people:        
#        try: 
#        for filter in list(filters.keys()): # прохождение по запрашиваемым фильтрам
#            if str(row[filter]) != str(filters[filter]):
#                print(row)
#                del people[row['row']]
#people.append('\t\t')
#print(people)

@app.route('/s')
@app.route('/create_resident')
def create_resident():
    return render_template('create_resident.html')

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
    
@app.route('/')
def testing():
    records = sheet.get_all_records()
    
    # Форматируем как текст с переносами
    text_response = "\n".join(str(record) for record in records)
    return Response(text_response, mimetype='text/plain')


#  #############  ###      ###      #############
#       ###         ##    ###            ###
#       ###          ##  ###             ###
#       ###            ####              ###
#       ###            ###               ###
#       ###          ####                ###


'''
  #############  ###      ###      #############
       ###         ##    ###            ###
       ###          ##  ###             ###
       ###            ####              ###
       ###            ###               ###
       ###          ####                ###
'''


@app.route('/user/<name>')
def user_page(name):
    records=sheet.get_all_records()
    list_of_users=[]
    for i in range(len(records)):
        
        if name in str(records[i]['ФИО']):
            list_of_users.append(records[i])
        else:
            pass
            #print (f'{name} is not in sheet \n {records[i]['ФИО']}') 
    print(list_of_users)
    return render_template('user_page.html',list_of_users=list_of_users)

if __name__ == "__main__":
    app.run(debug=True)
# Открытие таблицы

