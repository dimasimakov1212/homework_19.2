from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_product_categories():
    """
    Получает список категорий товаров
    """
    if settings.CACHE_ENABLED:
        key = 'category_list'  # ключ, по которому получаем список категорий
        category_list = cache.get(key)  # получаем данные из кэша
        if category_list is None:
            category_list = Category.objects.all()  # получаем все категории товаров
            cache.set(key, category_list)  # заносим список категорий в кэш
    else:
        category_list = Category.objects.all()

    return category_list
