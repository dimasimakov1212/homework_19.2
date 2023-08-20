from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from pytils.translit import slugify

from catalog.models import Product, Blog


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
    Выводит информаццию о 5 последних товарах на главную страницу вместо функции product_show
    """

    model = Product
    queryset = Product.objects.all().order_by('-pk')[:5]  # получаем 5 последних товаров
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        """
        Выводит контекстную информацию в шаблон
        """
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['title_2'] = 'лучшие товары для вас'
        return context


# def product_show(request):
#     """
#     Выводит 5 последних товаров на главную страницу
#     """
#
#     product_list = Product.objects.all().order_by('-pk')[:5]  # получаем 5 последних товаров
#
#     # задаем контекстный параметр для вывода на страницу
#     context = {
#         'products_list': product_list,
#         'title': 'Главная'
#     }
#
#     # вывод выбранных товаров в консоль
#     for product in product_list:
#         print(product)
#
#     return render(request, 'catalog/home.html', context)


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
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Карточка товара'
        return context


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
        context['title_2'] = 'полезные статьи'
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
        context['title_2'] = 'Просмотр статьи'
        return context

    def get_object(self, queryset=None):
        """
        Считает количество просмотров статьи
        """
        self.object = super().get_object(queryset)
        self.object.blog_views_count += 1
        self.object.save()

        return self.object


class BlogCreateView(CreateView):
    """
    Выводит форму создания статьи
    """
    model = Blog
    fields = ('blog_title', 'blog_text',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        """
        Реализует создание Slug — человекопонятный URL
        """
        if form.is_valid():
            new_article = form.save()
            new_article.blog_slug = slugify(new_article.blog_title)
            new_article.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """
    Выводит форму редактирования статьи
    """
    model = Blog
    fields = ('blog_title', 'blog_text',)

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
