from django.urls import path

from catalog.views import index, contact, product_show

urlpatterns = [
    path('', index),
    path('contacts/', contact),
    path('home/', product_show),
]
