from django import forms
from .models import User, Tools_table, Profile, Qr_table

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'komanda')


class Qr_tableForm(forms.ModelForm):
    class Meta:
        model = Qr_table
        fields = ('qr_id',)
