from django.urls import path
from django.views.decorators.cache import cache_page

from catalog import views
from catalog.views import contact, ProductListView, ProductDetailView, BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView, ProductCreateView, ProductUpdateView
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(ProductListView.as_view()), name='home'),
    path('contacts/', contact, name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_article'),
    path('create/', BlogCreateView.as_view(), name='create_article'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_article'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_article'),
]
