from django.contrib import admin

from catalog.models import Product, Category, Blog, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы товаров в админку
    """
    list_display = ('id', 'product_name', 'product_category', 'product_price',)
    list_filter = ('product_category',)
    search_fields = ('product_name', 'product_description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы категорий товаров в админку
    """
    list_display = ('id', 'category_name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы статей блога в админку
    """
    list_display = ('blog_title', 'blog_date_creation', 'blog_views_count', 'blog_is_active',)
    list_filter = ('blog_title',)
    search_fields = ('blog_title', 'blog_text',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """
    Описывает параметры для вывода таблицы версий админку
    """
    list_display = ('product', 'version_number', 'version_name', 'is_active',)
    list_filter = ('version_number',)
    search_fields = ('version_number', 'version_name',)
