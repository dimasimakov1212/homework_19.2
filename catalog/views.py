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

    return render(request, 'catalog/contacts.html')


def product_show(request):
    """
    Выводит 5 последних товаров на страницу
    """

    products_all = Product.objects.all()  # получаем весь список товаров

    num_prod = len(products_all)  # определяем количество товаров
    product_list = []  # задаем список для вывода на страницу

    # отбор последних 5 товаров по id
    for product_id in range(num_prod, num_prod - 5, -1):
        for product in products_all:
            if product.id == product_id:
                product_list.append(product)
                break

    # задаем контекстный параметр для вывода на страницу
    context = {
        'products_list': product_list
    }

    # вывод выбранных товаров в консоль
    for product in product_list:
        print(product)

    return render(request, 'catalog/home.html', context)
