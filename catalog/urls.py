from django.urls import path

from catalog.views import index, contact, product_show

urlpatterns = [
    path('', product_show),
    # path('', index),
    path('contacts/', contact),

]
