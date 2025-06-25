'''Функции взаимодействия с базой данных в Google sheets.
    sheet содержит данные о используемой таблице, изначально пуст, заполняется функцией initiate или использует базовый ключ.


'''
import gspread
from google.oauth2.service_account import Credentials
import time
from gspread_formatting import *

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
client = gspread.authorize(CREDS)
sheet=''
sheet_key_default='1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA'
  

global structure
structure=['ФИО','комната','user_id']

def initiate(sheet_key=sheet_key_default):
    '''Инициализирует подключение сервера к таблице, использует ключ.
    Возвращает объект таблицы.
    По умолчанию используются базовый ключ.'''
    sheet = client.open_by_key(sheet_key).sheet1
    return sheet


def print_data(filters={'комната':617},sheet=''):
    '''Выводит запрашиваемые данные, пока что только по комнате.
    Запрашивает фильтр, данные для вывода и объект таблицы.
    Выводит список требуемых данных.
    По умолчанию использует базовый ключ таблицы.'''
    
    filters_keys=[]
    print(filters)
    try:
        worksheet = sheet.get_all_records()
    except:
        print(f"Таблица не выбрана, возвращение в начало.")
        #worksheet = initiate().get_all_records()
        return
    
    titles=sheet.row_values(1)
    print(titles,'\n')
    people=[]
    for filter in list(filters.keys()):
        print(filter+':')
        if filter in titles:
                filters_keys.append(filter)
                print('\n\nФильтры в Таблице\n\n')
                
        else:
            print(f'Фильтра {filter} нет в таблице')
    print(filters)


    for i in range(len(worksheet)):
        #print(worksheet[i][filter],'\t\t',  filters[filter])
        try: 
            
            if str(worksheet[i][filter]) == str(filters[filter]):
                people.append(worksheet[i]['user_id'])    
            print(people)
        except: 
            print('\n\n Ошибка Фильтра\n\n')
            return





def add_people_request(sheet=sheet):
    '''Обработка пользователем.\n Создает в таблице новую строку с данными проживающего.
    Пока что запрашивает данные через input и отправляет dict с данными о пользователе на сервер.'''
    sheet=sheet
    try:
        worksheet = sheet.get_all_records()
    except:
        print(f"sheet doesn't exist, opening default database {initiate().spreadsheet.title}")
        worksheet = initiate().get_all_records()
        exit
    new_people={}
    for cell in worksheet.row_values(1):
        info=str(input(f'Введите {(cell)}: \n'))
        #print(sheet.find(cell).value)
        new_people[worksheet.find(cell).value]=info
    print('Данные переданы администратору!')
    return new_people


def add_people_master(people_data):
    time.sleep(3)
    print('\n\nПоступил запрос на обработку:\n')
    time.sleep(3)
    for title in people_data:
        print(f'{title}: {people_data[title]}')
        time.sleep(1)
    request =input('\n Что делать с данными?\n 1- отправить на сервер, 2 - отклонено\n')
    match request:
        case '1': send_to_server(people_data)
        case '2': print('Запрос отклонен\n')
        case '': print('Что-то какая-то #%!~*\n') 


def send_to_server(people_data={},sheet=sheet):
    print('Запрос отправлен на сервер...\n')
    sheet=sheet
    try:
        worksheet = sheet.get_all_records()
    except:
        print(f"sheet doesn't exist, opening default database {initiate().spreadsheet.title}")
        worksheet = initiate().get_all_records()
        exit
    send_data=[]
    
    for title in people_data:
        send_data.append(people_data[title])
    worksheet.append_row(send_data)
    time.sleep(1)
    print('Запрос обработан!\t')


def current_sheet(sheet):
    '''Определение текущей таблицы'''
    sheet=sheet
    try:
        worksheet = sheet.spreadsheet
        print(worksheet.title)
    except:
        print(f"sheet doesn't exist")
        #worksheet = initiate().spreadsheet
        exit
    #print(worksheet.title)


def clear_current_sheet(sheet):
    '''Очистка ключа текущей таблицы для переключения'''
    sheet=sheet
    try:
        worksheet = sheet.get_all_records()
        print(f'Текущая таблица :{sheet.spreadsheet.title} Отключена. \n Для дальнейшей корректной работы подключите таблицу.')
    except:
        print(f"Текущей таблицы нет.\n Для дальнейшей корректной работы подключите таблицу.")
        #worksheet = initiate().spreadsheet
        exit
    sheet=''
    return sheet


check=True
def server_process(check,sheet):
    '''Аналогия сервера для тестировки, вряд ли будет использоваться на релизе.'''
    while (check):
        
        
        
        s1=input(f'''Выберите действие: \n1 - вывод комнаты\n2 - добавление\n11-Активация таблицы \n3-Проверка текущей таблицы\n33 - Очистка текущей таблицы\n0 - выход\n''')
        match s1:
            case '1': print_data({'комната':input('Введите номер комнаты:\n')},sheet)
            case '2': 
                add_people_master(add_people_request(sheet))
            case '11': 
                s2=input(f'Выберите таблицу:\n')
                match s2:
                    case '1':
                        sheet=initiate('1UD0ZqwPg11p4-dGnj84K16eAGtun4NZMfL_SQgkgYzE')
                    case '2':
                        sheet=initiate('1baoDiv8FVUQ6Khk9DZpiaiBh1N0eqgzo-K9P3DogbNA')    
            case '3': 
                print('Проверка текущей таблицы \n')
                current_sheet(sheet)
            case '33':
                sheet =clear_current_sheet(sheet)
            case '0': 
                print('Пока-пока!\n')
                check=False


############################################################################
server_process(check,sheet)


