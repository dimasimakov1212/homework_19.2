from django.urls import path

from catalog import views
from catalog.views import contact, ProductListView, ProductDetailView, BlogListView, BlogDetailView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    # path('', product_show, name='home'),
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contact, name='contacts'),
    # path('product/', product, name='product'),
    # path(r'^objects/(?P<product_id>\w+)/$', product, name='product'),
    # path('<int:product_id>/product/', product, name='product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_article'),
]
