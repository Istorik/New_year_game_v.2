from django.contrib import admin

from .models import Ulika_table, Tools_table, Profile, Qr_table

# Register your models here.

admin.site.register(Ulika_table)
admin.site.register(Tools_table)
admin.site.register(Profile)
admin.site.register(Qr_table)
