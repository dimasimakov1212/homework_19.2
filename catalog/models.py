from datetime import date

from django.db import models
from django.db.models import SET_DEFAULT, SET_NULL

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    """
    Класс для создания категорий товаров
    """
    category_name = models.CharField(max_length=150, verbose_name='Категория')
    category_description = models.CharField(max_length=150, verbose_name='Описание')

    # is_active = models.BooleanField(default=True, verbose_name='учится')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Категории'  # Настройка для наименования набора объектов
        ordering = ('category_name',)  # сортировка по наименованию


class Product(models.Model):
    """
    Класс для создания товаров
    """
    product_name = models.CharField(max_length=150, verbose_name='Наименование')
    product_description = models.CharField(max_length=150, verbose_name='Описание')
    product_preview = models.ImageField(upload_to='catalog/', verbose_name='Превью', **NULLABLE)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
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


class Version(models.Model):
    """
    Класс для создания версии товароа
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(default=1, blank=True, verbose_name='Номер версии')
    version_name = models.CharField(max_length=150, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Текущая версия')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.product} {self.version_number}'

    class Meta:
        verbose_name = 'Версия'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Версии'  # Настройка для наименования набора объектов
        ordering = ('version_number',)  # сортировка по номеру версии


class Blog(models.Model):
    """
    Класс для ведения блога
    """
    blog_title = models.CharField(max_length=150, verbose_name='Заголовок')
    blog_text = models.TextField(verbose_name='Содержимое')
    blog_preview = models.ImageField(upload_to='catalog/', verbose_name='Превью', **NULLABLE)
    blog_slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    blog_date_creation = models.DateField(auto_now=False, auto_now_add=True, verbose_name='Дата создания')
    blog_is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
    blog_views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.blog_title}'

    class Meta:
        verbose_name = 'Статья'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Статьи'  # Настройка для наименования набора объектов
        ordering = ('blog_title',)  # сортировка по наименованию
