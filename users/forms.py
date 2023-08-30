from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
