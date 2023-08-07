from django.urls import path

from catalog import views
from catalog.views import index, contact, product_show, product
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', product_show, name='home'),
    # path('', index),
    path('contacts/', contact, name='contacts'),
    # path('product/', product, name='product'),
    # path(r'^objects/(?P<product_id>\w+)/$', product, name='product'),
    path('<int:product_id>/product/', product, name='product'),

]
