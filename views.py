from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, request
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db import transaction

from random import randint, choice

from .models import Ulika_table, Qr_table, Tools_table, UserUlikaFead, Profile
from .forms import UserForm, ProfileForm, Qr_tableForm, SignUpForm, FormLupa, FormPhoto, FormHim, FormDictofon

import pyqrcode	# sudo pip3 install pyqrcode


# Create your views here.

def index(request):
    return render(request, 'newYearGame/index.html')


def cabinet(request):

    if Profile.objects.filter(user=request.user, time_fin__isnull=False):
        return HttpResponse("Вы закончили игру")
   
    if request.POST:
        form = FormOtvet(request.POST)
        if form.is_valid():
            form = form.cleaned_data.get('type_slot')
            if len(form) == 2 and form.count('4') == 1 and form.count('2') == 1:
                messages.success(request, ('Похититель пойман'))
                Profile.objects.filter(user=request.user).update(time_fin = timezone.now())
            else:
                messages.error(request, ('Не верно'))
        else:
            messages.success(request, (form.errors))

    fin = ""
    ulika = UserUlikaFead.objects.filter(user_id=request.user, type_slot=0)
    if len(UserUlikaFead.objects.filter(user_id=request.user)) >= 42:
        fin = [
            'Первый преступник пил воду на месте преступления',
            'Второй преступник держит зебру',
            'Саурон пришел с красными перчатками',
            'Бармалей оставил свою собаку у входа на территорию школы.',
            'Хозяин зеленого плаща пьет кофе.',
            'Анонимус пьёт только чай.',
            'Кто-то в зеленом плаще зашел сразу после персонажа в белых ботинках.',
            'Любитель барбарисок разводит улиток.',
            'Тот кто пришел с желтым зонтиком был с Чупа-Чупсом.',
            'Тот кто пришел третим пьёт молоко.',
            'Гринч пришел первым, а сразу за ним кто в синих штанах.',
            'Тот кто пришел вместе с хозяином лошади, любитель Чупа-Чупсов.',
            'Любитель желатиновых мишек пьет апельсиновый сок.',
            'Снеговик ест конфеты «Коровка».'
        ]
        tools = ['']
        form = FormOtvet(request.POST)
    else:
        tools = Tools_table.objects.filter(user_id=request.user)
        form = ""

        return render(request, 'newYearGame/ulika_list.html', {
            'ulika': ulika,
	    'tools': tools,
	    'fin':fin,
	    'form':form,
        })

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


@login_required
def ulika(request, pk):
    ''' выводим улику в соответсвии с id
    '''

    posts = get_object_or_404(Ulika_table, idUlika=pk)

    if request.POST:
        lupa = FormLupa(request.POST)
        Dictofon = FormDictofon(request.POST)
        Him = FormHim(request.POST)
        Photo = FormPhoto(request.POST)

        if lupa.is_valid():
            lupa = UserUlikaFead(user_id=request.user, id_Qr=posts, type_slot=1)
            lupa.save(force_insert=True)

        if Dictofon.is_valid():
            Dictofon = UserUlikaFead(user_id=request.user, id_Qr=posts, type_slot=2)
            Dictofon.save(force_insert=True)

        if Him.is_valid():
            Him = UserUlikaFead(user_id=request.user, id_Qr=posts, type_slot=3)
            Him.save(force_insert=True)

        if Photo.is_valid():
            Photo = UserUlikaFead(user_id=request.user, id_Qr=posts, type_slot=4)
            Photo.save(force_insert=True)

        messages.success(request, ('Улика изучена'))

    fild = UserUlikaFead.objects.filter(user_id=request.user, id_Qr=posts, type_slot=0)
    if not fild:
        fild = UserUlikaFead(user_id=request.user, id_Qr=posts)
        fild.save(force_insert=True)

    status = 100
    status_full, status_user = 0, 0

    ''' status_full, status_user = 0
        Если у улики есть материал изучаемый инструментом Х
            status_full += 1 
            Если Игрок изучил улику с помощью интрумента Х
                status_user += 1
                Х = posts.Х
            Иначе Если у игрока есть инструмент Х
                form.Х
        иначе Х = ""
    '''
    formLupa = ""
    formPhoto = ""
    formHim = ""
    formDictofon = ""

    # Лупа
    if posts.ulikaLupa:
        status_full += 1
        if UserUlikaFead.objects.filter(user_id=request.user, id_Qr=posts, type_slot=1):
            status_user += 1
            formLupa = posts.ulikaLupa

        elif Tools_table.objects.filter(user_id=request.user, type_slot=1):
            formLupa = FormLupa()


    # Фотоаппаратом
    if posts.ulikaPhoto:
        status_full += 1
        if UserUlikaFead.objects.filter(user_id=request.user, id_Qr=posts, type_slot=4):
            status_user += 1
            formPhoto = posts.ulikaPhoto

        elif Tools_table.objects.filter(user_id=request.user, type_slot=4):
            formPhoto = FormPhoto()

    #  Набором Криминалиста
    if posts.ulikaHim:
        status_full += 1
        if UserUlikaFead.objects.filter(user_id=request.user, id_Qr=posts, type_slot=3):
            status_user += 1
            formHim = posts.ulikaHim
        elif Tools_table.objects.filter(user_id=request.user, type_slot=3):
            formHim = FormHim()

    #  Диктафоном
    if posts.ulikaDictofon:
        status_full += 1
        if UserUlikaFead.objects.filter(user_id=request.user, id_Qr=posts, type_slot=2):
            status_user += 1
            formDictofon = posts.ulikaDictofon
        elif Tools_table.objects.filter(user_id=request.user, type_slot=2):
            formDictofon = FormDictofon()

    code = pyqrcode.create('http://qvest.asspo.ru/{}/ulika'.format(pk))
    image = code.png_as_base64_str(scale=6)

    return render(
        request,
        'newYearGame/ulika.html',
        {
            'posts': posts,
            'status': status_user/status_full*100,
            'formLupa': formLupa,
            'formPhoto': formPhoto,
            'formHim': formHim,
            'formDictofon': formDictofon,
            'qrc': image,
        })

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
        ('10', 'Мусор'), ('11', 'Мусор'), ('12', 'Мусор'), ('13', 'Мусор'), ('14', 'Мусор'),
        ('15', 'Мусор'), ('16', 'Мусор'), ('17', 'Мусор'), ('18', 'Мусор'), ('19', 'Мусор'), ('20', 'Мусор'),
    )

    post = get_object_or_404(Qr_table, qr_id=pk)
    test = Tools_table.objects.filter(user_id=request.user, id_Qr=post)

    if test:
        text = 'Вы уже здесь были</br> И нашли <b>{}</b>'.format(test[0].get_type_slot_display())

    else:
        a = list(range(1, 21))
        user_loot_list = Tools_table.objects.filter(user_id=request.user)
        if len(user_loot_list) > 19:return render(request, 'newYearGame/loot.html', {'text': 'Вы нашли все, что можно было найти'})
        l = []
        for i in user_loot_list: l.append(int(i.type_slot))
        c = list(set(a) - set(l))
        loot = choice(c)
        p = Tools_table(user_id=request.user, id_Qr=post, type_slot=loot)
        p.save(force_insert=True)

        text = 'Покапавшись, Вы нашли </br> <b>{}</b>'.format(type_slot_list[loot-1][1])

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
            messages.error(request, ('Пожалуйста, исправьте ошибки.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
