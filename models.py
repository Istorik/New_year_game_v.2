from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)
    location = models.CharField('Класс', max_length=8, blank=True)
    komanda = models.TextField('Помощники')
    time_fin = models.DateTimeField("Время окончания игры", blank=True, null=True)

    def finish(self):
        self.time_fin = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Qr_table(models.Model):
    qr_id = models.IntegerField('Номер QR')

    class Meta:
        verbose_name = 'QR'
        verbose_name_plural = 'QR'

    def __str__(self):
        return self.qr_id


class Tools_table(models.Model):
    ''' Таблица с лутом, во сколько, кто, на каком QR и что нашел.
        id_User - кто нашел
        id_Qr - на каком QR коде нашел
        id_item - что нашел
        times - во сколько нашел
        spent - наличие в инвентаре
    '''

    user_id = models.ForeignKey(
        User,
        verbose_name="Команда нашедшая qr-code",
        on_delete=models.SET_NULL,
        null=True
    )
    id_Qr = models.ForeignKey(
        Qr_table,
        verbose_name="Найденный Qr",
        on_delete=models.SET_NULL,
        null=True
    )

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

    type_slot = models.CharField('номер инструмента',
        choices=type_slot_list,
        default=1,
        max_length=64)
    times = models.DateTimeField("Время нахождения", auto_now_add=True)
    spent = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Найденный инструмент'
        verbose_name_plural = 'База Найденных инструментов'

    def __str__(self):

        return "{} [{}] {} {}".format(
            self.user_id.username,
            self.get_type_slot_display(),
            self.times,
            self.spent,
        )

class Ulika_table(models.Model):
    ''' Таблица с уликами
        14 штук
    '''
    idUlika = models.IntegerField(default=0)
    ulikaName = models.CharField('Название улики', max_length=64)
    ulikaMesto = models.CharField('Место нахождения', max_length=128)
    ulikaText = models.TextField('Описание предмета')
    ulikaLupa = models.TextField('Описание после изучения Лупой', blank=True)
    ulikaPhoto = models.TextField('Описание после изучения Фотоаппаратом', blank=True)
    ulikaHim = models.TextField('Описание после изучения Набором Криминалиста', blank=True)
    ulikaDictofon = models.TextField('Описание после изучения Диктафоном', blank=True)
    ulikaImg = models.CharField('Изображение', max_length=128)

    class Meta:
        verbose_name = 'Улика'
        verbose_name_plural = 'Улики'

    def __str__(self):
        return self.ulikaName

class UserUlikaFead(models.Model):
    ''' Кто, во сколько и какую улику нашел. чем изучил
    '''
    type_slot_list = (
        ('0', 'Нашел'),
        ('1', 'Лупа'),
        ('2', 'Диктофон'),
        ('3', 'Химический набор'),
        ('4', 'Сканер'),
    )
    user_id = models.ForeignKey(
        User,
        verbose_name="Команда нашедшая qr-code улики",
        on_delete=models.SET_NULL,
        null=True
    )
    times = models.DateTimeField("Время нахождения", auto_now_add=True)
    id_Qr = models.ForeignKey(
        Ulika_table,
        verbose_name="Найденный Qr",
        on_delete=models.SET_NULL,
        null=True
    )
    type_slot = models.CharField('Чем поюзал',
        choices=type_slot_list,
        default=0,
        max_length=64)

    class Meta:
        verbose_name = 'Поюзал улику'
        verbose_name_plural = 'Поюзал улику'

    def __str__(self):
        return "[{}] {} | {}".format(
            self.user_id.username,
            self.id_Qr.ulikaName,
            self.get_type_slot_display(),
            #1,1,1

        )
