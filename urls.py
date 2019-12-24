from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('<pk>/ulika', views.ulika, name='ulika'),
    path('<pk>/loot', views.loot, name='loot'),
    path('qr', views.qr, name='qr'),
]