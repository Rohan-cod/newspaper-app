from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('username', 'nick_name', 'dob', 'gender', 'email', 'age', 'pic',)

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'nick_name', 'gender', 'email', 'age', 'pic',)

