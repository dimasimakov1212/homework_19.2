from django.urls import path

from catalog.views import index, contact, product_show
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', product_show, name='home'),
    # path('', index),
    path('contacts/', contact, name='contacts'),

]
