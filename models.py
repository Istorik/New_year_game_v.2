from django.db import models

# Create your models here.
# Тест коммит


class Tools_table(models.Model):
    ''' id_User - кто нашел
        id_Qr - на каком QR коде нашел
        id_item - что нашел
        times - во сколько нашел
        spent - наличие в инвентаре
    '''
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

    id_item = models.IntegerField(default=0)
    # id_User - кто нашел
    # id_Qr - на каком QR коде нашел
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
        return "[{}] {}".format(
            self.id_item,
            self.item_name,
        )
