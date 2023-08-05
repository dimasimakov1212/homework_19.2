import datetime

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Product, Category


class Command(BaseCommand):
    """
    Класс очищает таблицы и заносит новые данные
    """

    def handle(self, *args, **options):

        # Product.objects.all().delete()  # очищаем таблицу товаров
        # Category.objects.all().delete()  # очищаем таблицу категорий товаров

        cursor = connection.cursor()  # создаем подключение к БД
        cursor.execute("TRUNCATE TABLE catalog_product RESTART IDENTITY")  # очищаем таблицу и сбрасываем нумерацию
        cursor.execute("TRUNCATE TABLE catalog_category RESTART IDENTITY")
        connection.close()  # закрываем соединение

        date_now = datetime.date.today  # текущая дата

        # список товаров
        products_list = [
            {'product_name': 'IPhone 10', 'product_description': 'Смартфон 5,5" 256Гб', 'product_category': 'Телефоны',
             'product_price': '95000.00', 'date_creation': date_now, 'date_changing': date_now},
            {'product_name': 'Ariston 201', 'product_description': 'Холодильник встраиваемый',
             'product_category': 'Холодильники', 'product_price': '65700.00', 'date_creation': date_now,
             'date_changing': date_now},
            {'product_name': 'Samsung 1012', 'product_description': 'Смартфон 5" 32Гб',
             'product_category': 'Телефоны', 'product_price': '10000.00', 'date_creation': date_now,
             'date_changing': date_now},
            {'product_name': 'Samsung 1015', 'product_description': 'Смартфон 5,5" 32Гб',
             'product_category': 'Телефоны', 'product_price': '12000.00', 'date_creation': date_now,
             'date_changing': date_now},
            {'product_name': 'Bosh H102', 'product_description': 'Холодильник двухкамерный',
             'product_category': 'Холодильники', 'product_price': '54000.00', 'date_creation': date_now,
             'date_changing': date_now},
            {'product_name': 'Sony 2754', 'product_description': 'Телевизор LCD 37"',
             'product_category': 'Телевизоры', 'product_price': '28000.00', 'date_creation': date_now,
             'date_changing': date_now}
        ]

        # список категорий товаров
        categories_list = [
            {'category_name': 'Телефоны', 'category_description': 'Устройства мобильной, проводной, спутниковой связи'},
            {'category_name': 'Телевизоры', 'category_description': 'Телевизионные приемники, смарт-телевизоры'},
            {'category_name': 'Холодильники', 'category_description': 'Холодильники, морозильные камеры'},
        ]

        # заполняем список товаров для добавления в БД
        products_for_create = []
        for product in products_list:
            products_for_create.append(Product(**product))

        # заполняем список категорий товаров для добавления в БД
        categories_for_create = []
        for category in categories_list:
            categories_for_create.append(Category(**category))

        # заносим данные в БД
        Product.objects.bulk_create(products_for_create)
        Category.objects.bulk_create(categories_for_create)
