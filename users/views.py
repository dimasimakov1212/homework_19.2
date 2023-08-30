from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """
    Контроллер регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Проверка валидности данных
        """
        new_user = form.save()
        send_mail(
            subject='Регистрация на портале',
            message='Вы зарегистрировались на нашей платформе',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    """
    Контроллер профиля пользователя
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Позволяет делать необязательным передачу pk объекта
        """
        return self.request.user
