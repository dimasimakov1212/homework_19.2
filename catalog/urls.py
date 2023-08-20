from django.urls import path

from catalog import views
from catalog.views import contact, ProductListView, ProductDetailView, BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    # path('', product_show, name='home'),
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contact, name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_article'),
    path('create/', BlogCreateView.as_view(), name='create_article'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_article'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_article'),
]
