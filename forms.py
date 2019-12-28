from django import forms
from .models import Tools_table, Profile, Qr_table, UserUlikaFead
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


class FormLupa(forms.ModelForm):
    CHOICES = [('1', 'Изучить'),
               ('0', 'Оставить')]
    type_slot = forms.ChoiceField(label='Лупа', choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = UserUlikaFead
        fields = ('type_slot',)

class FormPhoto(forms.ModelForm):
    CHOICES = [('4', 'Изучить'),
               ('0', 'Оставить')]
    type_slot = forms.ChoiceField(label='Сканер', choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = UserUlikaFead
        fields = ('type_slot',)

class FormHim(forms.ModelForm):
    CHOICES = [('3', 'Изучить'),
               ('0', 'Оставить')]
    type_slot = forms.ChoiceField(label='Химический набор', choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = UserUlikaFead
        fields = ('type_slot',)

class FormDictofon(forms.ModelForm):
    CHOICES = [('2', 'Изучить'),
               ('0', 'Оставить')]
    type_slot = forms.ChoiceField(label='Диктофон', choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = UserUlikaFead
        fields = ('type_slot',)

class FormOtvet(forms.Form):
    CHOICES = [
            ('0', 'Ананимус'),
            ('1', 'Бармалей'),
            ('2', 'Гринч'),
            ('3', 'Саурон'),
            ('4', 'Снеговик')
             ]

    type_slot = forms.MultipleChoiceField(label='Отметьте двух похитителей', 
            choices=CHOICES,
            widget=forms.CheckboxSelectMultiple,)
