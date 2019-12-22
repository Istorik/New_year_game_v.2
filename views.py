from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import transaction
from .models import Ulika_table

from .forms import UserForm, ProfileForm

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

        'Lupa': '',
        'Photo': '',
        'Him': '',
        'Dictofon': '',
    }

    posts = get_object_or_404(Ulika_table, pk=pk)

    status = 15

    return render(request, 'newYearGame/ulika.html', {'posts': posts, 'status': status})

# def musor(User, Qr):
#     '''
#         Уже сканировал
#             объект есть
#                 вернуть мусор
#             объекта нет
#                 вернуть то что находил
#         еще не сканировал
#             unstrument()
#     '''
#     pass

def loot(request, pk):
    ''' генерируем список из не найденных инструментов
                выводим случайный объект
    '''

    # если юзер + qr = True то text = 'Вы не нашли ни чего интересного.'
    # иначе вернуть случайны из массива инструментов

    text = 'Вы не нашли ни чего интересного.'
    return render(request, 'newYearGame/loot.html', {'text': text})

    pass

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Ваш профиль был успешно обновлен!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })