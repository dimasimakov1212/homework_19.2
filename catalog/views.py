from django.shortcuts import render


def index(request):

    return render(request, 'catalog/home.html')


def contact(request):

    return render(request, 'catalog/contacts.html')
