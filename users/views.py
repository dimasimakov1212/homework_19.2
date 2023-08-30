from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.forms import UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    """
    Контроллер регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
