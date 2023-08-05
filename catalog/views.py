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

    prod = Product.objects.all()
    context = {
        'products_list': prod
    }
    for product in prod:
        print(product)

    return render(request, 'catalog/home.html', context)
