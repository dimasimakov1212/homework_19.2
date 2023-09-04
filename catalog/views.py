from django.contrib.auth import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

import catalog
from catalog.forms import ProductForm, BlogForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Blog, Version


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


class ProductListView(ListView):
    """
    Выводит информаццию о последних 6 товарах на главную страницу
    """

    model = Product
    # queryset = Product.objects.all().order_by('-pk')[:6]  # получаем 6 последних товаров

    template_name = 'catalog/home.html'

    def get_queryset(self):

        user = self.request.user

        if user.is_authenticated:  # для зарегистрированных пользователей
            if user.is_staff or user.is_superuser:  # для работников и суперпользователя
                queryset = super().get_queryset().order_by('-pk')[:6]

            else:  # для остальных пользователей
                queryset = super().get_queryset().filter(
                    is_active=True).order_by('-pk')[:6]
        else:  # для незарегистрированных пользователей
            queryset = super().get_queryset().filter(
                is_active=True).order_by('-pk')[:6]
        return queryset

    # def get_queryset(self, *args, **kwargs):
    #     """
    #     Выводит в список только товары конкретного пользователя,
    #     либо если пользователь не авторизован - выводит все товары
    #     """
    #     queryset = super().get_queryset(*args, **kwargs)
    #
    #     try:
    #         queryset = queryset.filter(owner=self.request.user)
    #
    #     except TypeError:
    #         queryset = queryset.all().order_by('-pk')[:5]  # выводит последние 5 товаров
    #
    #     return queryset

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ProductListView, self).get_context_data(**kwargs)

        for product in context['product_list']:
            active_version = Version.objects.filter(product=product, is_active=True).last()
            if active_version:
                product.active_version_number = active_version.version_number
                product.active_version_name = active_version.version_name
            else:
                product.active_version_number = None
                product.active_version_name = None

        context['title'] = 'Главная'
        context['title_2'] = 'лучшие товары для вас'

        return context


class ProductDetailView(DetailView):
    """
    Выводит информаццию об одном, выбранном на главной странице, товаре вместо функции product
    """
    model = Product
    # template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super().get_context_data(**kwargs)

        active_version = Version.objects.filter(product=self.object, is_active=True).last()
        if active_version:
            context['active_version_number'] = active_version.version_number
            context['active_version_name'] = active_version.version_name
        else:
            context['active_version_number'] = None
            context['active_version_name'] = None

        context['title'] = 'Карточка товара'

        return context


class ProductCreateView(CreateView):
    """
    Выводит форму создания продукта
    """
    model = Product
    form_class = ProductForm

    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """
    Выводит форму редактирования товара
    """
    model = Product
    form_class = ProductForm

    success_url = reverse_lazy('catalog:home')

    def get_form_class(self):
        product = self.get_object()
        user = self.request.user
        print('get_form')

        if user.is_staff:
            return ProductModeratorForm

        elif product.owner == user:
            print('tut')
            return ProductForm

        return super().get_form_class()

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context_data = super().get_context_data(**kwargs)

        try:
            active_version = Version.objects.filter(product=self.object, is_active=True).last()

            # active_version_number = active_version.version_number

        except AttributeError:
            pass

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """
        Проверяем данные на правильность заполнения
        """
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """
    Выводит информаццию о статьях блога
    """

    model = Blog
    template_name = 'catalog/blog_list.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Полезные статьи'
        return context

    def get_queryset(self, *args, **kwargs):
        """
        Выводит в список только опубликованные статьи
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(blog_is_active=True)

        return queryset


class BlogDetailView(DetailView):
    """
    Выводит информаццию о статье
    """
    model = Blog

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Просмотр статьи'
        return context

    def get_object(self, queryset=None):
        """
        Считает количество просмотров статьи
        """
        self.object = super(BlogDetailView, self).get_object(queryset)
        self.object.blog_views_count += 1
        self.object.save()

        return self.object


class BlogCreateView(CreateView):
    """
    Выводит форму создания статьи
    """
    model = Blog
    form_class = BlogForm
    # fields = ('blog_title', 'blog_text', 'blog_preview')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        """
        Реализует создание Slug — человекопонятный URL
        """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        if form.is_valid():
            new_article = form.save()
            new_article.blog_slug = slugify(new_article.blog_title)
            new_article.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Создание статьи'
        return context


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Выводит форму редактирования статьи
    """
    model = Blog
    form_class = BlogForm
    permission_required = 'catalog.change_blog'

    def form_valid(self, form):
        """
        Реализует создание Slug — человекопонятный URL
        """
        if form.is_valid():
            new_article = form.save()
            new_article.blog_slug = slugify(new_article.blog_title)
            new_article.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        Получает адрес перенаправления после редактирования материала
        """
        return reverse('catalog:blog_article', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Изменение статьи'
        return context


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Выводит форму удаления статьи
    """
    model = Blog
    permission_required = 'catalog.delete_blog'
    success_url = reverse_lazy('catalog:blog_list')

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['title_2'] = 'Удаление статьи'
        return context
