
with open('alive.txt','r',encoding="utf-8") as f:
    alive = f.readlines()
class People:
    ''' Человек, имеющий следующие данные: UID, ФИО, группа '''
    def __init__(self,id='0000',surname='Иванов', name='Иван', secondname='Иванович'):
        self.user_id=id
        self.surname=surname
        self.name=name
        self.secondname=secondname
    
stepka=People()
print(stepka.name)
print(alive)