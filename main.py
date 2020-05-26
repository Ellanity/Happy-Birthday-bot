from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import json
import time
import random
import requests
import os
#Импорт библиотек завершен

session = requests.Session()  #Запрос на авторизацию
token = os.environ.get('HAPPY_BIRTHDAY_TOKEN')  #Специальный ключ(токен) доступа в переменной
vk_session = vk_api.VkApi(token = token)  #Отсыл токена для авторизации и начала сессии

longpoll = VkLongPoll(vk_session)  #Посылаем запрос типа longpool на сервер вк
vk = vk_session.get_api()

def Get_blocked_users_list():  #Получения списка пользователей, которым не требуется отсылать поздравление с днем рождения
    Blacklist_from_file = open('Blacklisted.txt', 'r')  #Открываем файл 'Blacklisted.txt' для чтения из него
    #Создаем переменную типа string для хранения в ней информации из файла, и помещаем туда информацию
    Blacklist_from_file_string_format = Blacklist_from_file.read()
    #Создаем список для хранения всех заблокированных id, который в последующем требуется вернуть(результат работы функции)
    Blacklist_from_file_list_format = []
    #Создаем переменную типа integer для записи в нее id из Blacklist_from_file_string_format и последующей передачи
    #в список Blacklist_from_file_list_format
    Id_for_block = 0;
    for Symbol in Blacklist_from_file_string_format:  #Посимвольно проходимся по строке с заблокированными id
        if(Symbol >= '0' and Symbol <= '9'):  #В случае, если символ является цифрой
            Id_for_block *= 10  #Имеющееся на данный момент значение в переменой мы домнажаем на 10
            Id_for_block += int(Symbol)  #А затем добавляем преобразованный в integer символ из строки
            #Тем самым пошагово воссоздавая id из string в integer
        elif(Symbol == ',' or Symbol == '.'):  #В случае если символ не является цифрой и означает конец предыдущего id
            Blacklist_from_file_list_format.append(Id_for_block)  #Помещаем имеющийся на данный момент id типа integer
            #в список Blacklist_from_file_list_format, для последующей передачи
            Id_for_block = 0  #Устанавливаем нулевое значение для следующего id
    return Blacklist_from_file_list_format  #Передаем полученный нами список

def Get_Friend_list():  #Функция для получения друзей пользователя, с учетом тех, кому нне надо ничего отправлять
    #Получим файл json от серверов вк и преобразуем его в список
    Friends_list = json.loads(requests.get('https://api.vk.com/method/friends.get?user_id=&access_token={0}&v=5.42&lang={1}'.format(token,'ru')).text)['response']['items']

    #print (Friends_list)  #Полученный список id друзей пользователя

    Blocked_friends_list = Get_blocked_users_list()#Пользователи которым не будет отправляться поздравление(список)

    #print (Blocked_friends_list) #Для проверки списка заблокированных пользователей

    for Blocked in Blocked_friends_list:  #Главный (верхний/первый/коренной по иерархии) цикл, проходимся по блоклисту по одному элементу
        j = 0  #Начинаем счет элементов в френдлисте
        for Friend in Friends_list:  #Проходимся внутри главного цикла для нахождения идентичного элемента
            if (Blocked == Friend):  #При совадении
                Friends_list.pop(j)  #Удаляем из френдлиста найденный элемент
                j -= 1  #Так как один элемент удален, мы возращаем индексацию на единицу назад
            j += 1  #Перед переходом к следующему элементу во френдлисте увеличиваем индекс на один

    return (Friends_list) #Возвращаем имеющийся на данный момент френдлист пользователей, которые мы собираемся поздравлять

def Get_Birth_date(User_id):  #Проверка и получение даты рождения пользователя с определеным идентификационным номером
    #Получим всю доступную данному токену информацию об определенном аккаунте
    #print(User_id)
    #Отправим запрос на сервер вк, чтобы получить информацию о пользователе при помщи json файлов в список 'User'
    User = json.loads(requests.get('https://api.vk.com/method/users.get?user_ids={0}&fields=bdate&access_token={1}&v=5.42&lang={2}'.format(User_id, token, 'ru')).text)['response']
    #print(User)  #Полученная нами информация о данном пользователе (имеющим id = User_id)
    try:  #Пробуем
        Birth_date = (User[0]['bdate'])  #Из полученного от серверов списка достать дату рождения пользователя
        #Если у нас получается, то следующие 2 строки пропускае
    except:  #Иначе
        Birth_date = "0"  #Мы устонавливаем нулевое значение, отмечая тем самым, что дата рождения не указана
    return Birth_date  #Возвращаем из функции итоговую информацию о дате рождения в формате string

def The_comparison_of_dates(Try_date):  #Получение даты на текущий момент в формате "day:month" и ее сопоставление с другой датой

    Now = datetime.now()  #Получаем дату и время из библиотеки datetime
    Date = str(str(Now.day) + "." + str(Now.month))  #Дата на текущий момент в формате "day:month"
    Coincide = True  #Булевская переменная для возрата положительного или отрицательного результата функции

    #Проверим совпадают ли даты
    i = 0  #Создадим индекс для нумерации символов строк(дат)
    while i < len(Date): #Так как мы поздравляем с днем рождения, нам достаточно проверить совпадают ли день и месясяц
                        #Поэтому мы записывали текущую дату в определенном формате, который нам выдает сервер вк
                        #При помощи индекса проходимся от первого до последнего чаровского элемента строки нынешней даты
        if(Try_date[i] != Date[i]):  #Проверяем совпадают ли символы первой и второй строки имеющей одинаковые индексы
            Coincide = False  #Если нет, то даты не совпадают, и мы выдадем отрицательный результат работы функции
            i = len(Date)  #Чтобы цикл while прекратился, ставим значение индекса выше, чем то, до которого индекс идет
        i += 1  #В случае если символы совпали, мы просто переходим к следующим симвлам в строках
    return Coincide  #Возвращаем положительный или отрицательный результат работы функции

def Random_congratulation():  #Функция для получения случайного поздравления из списка, находящегося в файле 'Congratulation.txt'
    Random_line_with_congratulation = ""  #Переменная типа string, которую требуется вернуть с измененным значением
    All_congratulations = open('Congratulation.txt', 'r')  #Открываем файл, находящийся в той же папке, что и main.py
    Line_quantity = 0  #Переменная для подсчета количества строк в файле с поздравлениями
    for Line in All_congratulations:  #Начиная с первой строки, мы идем по файлу
        Line_quantity += 1  #Найдя новую строку, мы каждый раз добавляем 1 к общему количеству строк
    Random_line = random.randint(1, Line_quantity)  #Зная количество строк, мы выбираем случайную от 1 до Line_quantity
    All_congratulations.close()  #Закрываем файл
    All_congratulations = open('Congratulation.txt', 'r')  #Заново его открываем
    j = 0  #Создаем индекс для строк
    for Line in All_congratulations:  #Снова идем по всему файлу, на этот раз ищем нужную нам строку
        j += 1  #Чтоб не случился конфликт индексов, добавляем единицу при каждой новой строке
        if (j == Random_line):  #В случае если индекс строки совпал со случайно выбанным нами значением
            Random_line_with_congratulation = Line  #Мы записываем данную строку в переменную, созданную в начале функции
    return Random_line_with_congratulation  #Возвращаем случайную строку из файла 'Congratulation.txt'



while True:  #Начинаем бесконечный цикл для постоянной проверки даты и времени
    if (str(datetime.strftime(datetime.now(), "%H:%M:%S")) == "17:10:00"
            or str(datetime.strftime(datetime.now(), "%H:%M:%S")) == "17:10:01"
            or str(datetime.strftime(datetime.now(), "%H:%M:%S")) == "17:10:02"):
                #Раз в день начинаем проверку всех пользователей во френдлисте
        time.sleep(5);  #Ожидаем, чтобы исключить возможность выпонения программы несколько раз
        Friends_to_congratulate = Get_Friend_list()  #Получаем список друзей пользователся на данный момент и записываем их в новый список
        #print(Friends_to_congratulate)  #Убедиться, что все работает верно
        for User in Friends_to_congratulate:  #Проходимся по списку тех, кого надо поздравить
            dBirth = Get_Birth_date(User)  #Получаем дату рождения определенного пользователя из списка
            Result_of_comparison = The_comparison_of_dates(dBirth)  #Полученный результат после сравнения дат рождения и текущей(+/-)
            if (Result_of_comparison == True):  #Если даты совпали, то сегодня у пользователя день рождения
                print(1, User, dBirth)
                Message_text = Random_congratulation()
                vk_session.method('messages.send', {'user_id': User, 'message': Message_text, 'random_id': 0})
        time.sleep(82800)
