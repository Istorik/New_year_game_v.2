from django.shortcuts import render
from django.http import HttpResponse, request

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

def ulika(request):
    ''' выводим улику в соответсвии с id
    '''

    posts = {
        'id': 1,
        'ulikaImg': 'img',
        'ulikaMesto': 'Библиотека',
        'status': 49,
        'ulikaName': 'Пятно',
        'ulikaText': 'Темное пятно на скатерти',
        'Lupa': '',
        'Photo': '',
        'Him': '',
        'Dictofon': '',
    }
    return render(request, 'newYearGame/ulika.html', {'posts': posts})
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