from django.contrib.auth.models import User
from django import forms

# import models

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLogin(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput)

class CharacterUploadImage(forms.Form):
	image = forms.ImageField()
	# x = forms.IntegerFileld(label='X: ', default=0)
	# y = forms.IntegerFileld(label='Y: ', defualt=0)
