from django.urls import path

from catalog import views
from catalog.views import contact, ProductListView, ProductDetailView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    # path('', product_show, name='home'),
    path('', ProductListView.as_view(), name='home'),
    # path('', index),
    path('contacts/', contact, name='contacts'),
    # path('product/', product, name='product'),
    # path(r'^objects/(?P<product_id>\w+)/$', product, name='product'),
    # path('<int:product_id>/product/', product, name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),

]
