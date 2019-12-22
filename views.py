from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.db import transaction

from random import randint, choice

from .models import Ulika_table, Qr_table, Tools_table

from .forms import UserForm, ProfileForm, Qr_tableForm

import pyqrcode	# sudo pip3 install pyqrcode
import png	# sudo pip3 install pypng


# Create your views here.

def index(request):
    return HttpResponse("Добро пожаловать на нашу игру")

@user_passes_test(lambda u: u.is_superuser)
def qr(request):
    ''' создаем 28 qr кодов для поиска инструменат
    '''

    if request.method == "POST":
        for i in range(1, 29):
            j = randint(1000000, 9999999)
            p = Qr_table(qr_id = j,)
            p.save(force_insert=True)

    images = Qr_table.objects.all()

    image = []

    for row in images:
        code = pyqrcode.create('http://qvest.asspo.ru/{}/loot'.format(row.qr_id))
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

    posts = get_object_or_404(Ulika_table, idUlika=pk)

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
    type_slot_list = (
        ('1','Лупа'),
        ('2','Диктофон'),
        ('3','Химический набор'),
        ('4','Сканер'),
        ('5', 'Вода'),
        ('6', 'Гвоздь'),
        ('7', 'Йод'),
        ('8', 'Фенол Фталеин'),
        ('9', 'Керосин'),
        ('10', 'Мусор'),
        ('11', 'Мусор'),
        ('12', 'Мусор'),
        ('13', 'Мусор'),
        ('14', 'Мусор'),
        ('15', 'Мусор'),
        ('16', 'Мусор'),
        ('17', 'Мусор'),
        ('18', 'Мусор'),
        ('19', 'Мусор'),
        ('20', 'Мусор'),
    )

    post = get_object_or_404(Qr_table, qr_id=pk)
    test = Tools_table.objects.filter(user_id=request.user, id_Qr=post)

    if test:
        print(test)
        text = 'Вы уже здесь были</br> '
        return render(request, 'newYearGame/loot.html', {'text': text})
    else:
        a = list(range(1, 21))
        user_loot_list = Tools_table.objects.filter(user_id=request.user)
        if len(user_loot_list) > 19:return render(request, 'newYearGame/loot.html', {'text': 'Вы нашли все, что можно было найти'})
        l = []
        for i in user_loot_list: l.append(i.type_slot)

        c = list(set(a) - set(l))
        loot = choice(c)

        p = Tools_table(user_id=request.user, id_Qr=post, type_slot=loot)
        p.save(force_insert=True)

        print(loot)

        text = 'Покапавшись, Вы нашли </br> <b>{}</b>'.format(type_slot_list[loot-1][1])
        return render(request, 'newYearGame/loot.html', {'text': text})


    text = 'Вы не нашли ни чего интересного.'
    return render(request, 'newYearGame/loot.html', {'text': text})


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