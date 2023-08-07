from datetime import date

from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """
    Класс для создания товаров
    """
    product_name = models.CharField(max_length=150, verbose_name='Наименование')
    product_description = models.CharField(max_length=150, verbose_name='Описание')
    product_preview = models.ImageField(upload_to='catalog/', verbose_name='Превью', **NULLABLE)
    product_category = models.CharField(max_length=150, verbose_name='Категория')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    date_creation = models.DateField(auto_now=False, auto_now_add=True, verbose_name='Дата создания')
    date_changing = models.DateField(auto_now=True, auto_now_add=False, verbose_name='Дата последнего изменения')

    # is_active = models.BooleanField(default=True, verbose_name='учится')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.product_name} {self.product_price}'

    class Meta:
        verbose_name = 'Товар'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Товары'  # Настройка для наименования набора объектов
        ordering = ('product_name',)  # сортировка по наименованию


class Category(models.Model):
    """
    Класс для создания категорий товаров
    """
    category_name = models.CharField(max_length=150, verbose_name='Наименование')
    category_description = models.CharField(max_length=150, verbose_name='Описание')

    # is_active = models.BooleanField(default=True, verbose_name='учится')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Категории'  # Настройка для наименования набора объектов
        ordering = ('category_name',)  # сортировка по наименованию
