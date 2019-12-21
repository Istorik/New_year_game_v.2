from django.shortcuts import render
from django.http import HttpResponse, request

from .models import Ulika_table

import pyqrcode	# sudo pip3 install pyqrcode
import png	# sudo pip3 install pypng


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
    image = []
    for i in range(1, 29):
        code = pyqrcode.create('http://qvest.asspo.ru/cgi-bin/lut.py?idLut={}'.format(i))
        image.append(code.png_as_base64_str(scale=6))
    return render(request, 'newYearGame/qr_list.html', {'qrs': image})



def ulika(request, pk):
    ''' выводим улику в соответсвии с id
    '''

    posts = {
        'id': pk,
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

def loot(request, pk):
    ''' генерируем список из не найденных инструментов
                выводим случайный объект
    '''

    # если юзер + qr = True то text = 'Вы не нашли ни чего интересного.'
    # иначе вернуть случайны из массива инструментов

    text = 'Вы не нашли ни чего интересного.'
    return render(request, 'newYearGame/loot.html', {'text': text})

    pass