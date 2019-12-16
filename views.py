from django.shortcuts import render
from django.http import HttpResponse

from .models import Ulika_table



# Create your views here.

def index(request):
    return HttpResponse("Добро пожаловать на нашу игру")

def qr(request):
    ''' Найден qr код
        Тестим что это за код.
            мусор
                перенаправитиьт на musor
            улика
                перенаправить на улику
    '''
    pass

def ulika(User, Qr):
    ''' выводим улику в соответсвии с id
    '''

    posts = {
        'ulikaImg': '',
        'ulikaMesto': '',
        'status': '',
        'ulikaName': '',
        'ulikaText': '',
        'Lupa': '',
        'Photo': '',
        'Him': '',
        'Dictofon': '',
    }
    return render(request, 'newYearGame/ulika', {'posts': posts})
    pass

def musor(User, Qr):
    '''
        Уже сканировал
            объект есть
                вернуть мусор
            объекта нет
                вернуть то что находил
        еще не сканировал
            unstrument()
    '''
    pass

def unstrument(User, Qr):
    ''' генерируем список из не найденных инструментов
                выводим случайный объект


    '''
    pass