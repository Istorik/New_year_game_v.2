from django.contrib import admin

from .models import Ulika_table, Tools_table, Profile, Qr_table, UserUlikaFead

# Register your models here.

admin.site.register(Ulika_table)
admin.site.register(Tools_table)

admin.site.register(Qr_table)
admin.site.register(UserUlikaFead)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('first_name', 'last_name', 'location', 'user_time_start', 'time_fin')

    def user_time_start(self, obj):
        return obj.user.date_joined

    user_time_start.admin_order_field = 'user__date_joined'
