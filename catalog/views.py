from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Product


def index(request):

    return render(request, 'catalog/home.html')


def contact(request):
    """
    Получает контактные данные, котрые клиент вносит при регистрации
    """

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Новое сообщение от {name}({phone}): {message}')

    # задаем контекстный параметр для вывода на страницу
    context = {
        'title': 'Контакты'
    }

    return render(request, 'catalog/contacts.html', context)


def product_show(request):
    """
    Выводит 5 последних товаров на главную страницу
    """

    product_list = Product.objects.all().order_by('-pk')[:5]  # получаем 5 последних товаров

    # задаем контекстный параметр для вывода на страницу
    context = {
        'products_list': product_list,
        'title': 'Главная'
    }

    # вывод выбранных товаров в консоль
    for product in product_list:
        print(product)

    return render(request, 'catalog/home.html', context)


def product(request, product_id):
    """
    Выводит товар на отдельную страницу
    """

    product_info = Product.objects.get(pk=product_id)  # получаем данные товара по его id

    # задаем контекстный параметр для вывода на страницу
    context = {
        'title': 'Карточка товара',
        'product_info': product_info
    }

    return render(request, 'catalog/product.html', context)
