from django import forms
from .models import Tools_table, Profile, Qr_table
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'komanda')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(max_length=100, label='Фамилия')
    location = forms.CharField(max_length=100, label='Класс')
    komanda = forms.CharField(max_length=500, label='Команда', widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'location', 'komanda', 'password1', 'password2',)


class Qr_tableForm(forms.ModelForm):
    class Meta:
        model = Qr_table
        fields = ('qr_id',)
