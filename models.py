from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField('Класс', max_length=30, blank=True)
    komanda = models.TextField('Помощники', blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Qr_table(models.Model):
    pass

class Tools_table(models.Model):
    ''' id_User - кто нашел
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
        ('5', 'Мусор'),
        ('6', 'Гвоздь'),
        ('7', 'Йод'),
        ('8', 'Фенол Фталеин'),
        ('9', 'Керосин'),
        ('10', 'Вода'))

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
        return "{} {} {} {}".format(
            self.user_id,
            self.type_slot_list[self.type_slot],
            self.times,
            self.spent,


        )

class Ulika_table(models.Model):

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
        return "[{}] {}".format(
            self.idUlika,
            self.ulikaName,
        )