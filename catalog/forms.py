from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from catalog.models import Product, Blog, Version


class ProductForm(forms.ModelForm):
    """
     Создает форму для создания товара
    """

    class Meta:
        """
        Определяет параметры формы
        """
        model = Product

        exclude = ('date_creation', 'date_changing')  # выводит в форму все поля, кроме указанных

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """
        Проверяет корректность ввода названия товара
        """
        # задаем список запрещенных к использованию слов
        stop_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        cleaned_data = super().clean()

        name = self.cleaned_data['product_name']
        description = self.cleaned_data['product_description']

        for item in stop_list:
            if item in name.lower():
                raise forms.ValidationError(f'Слово "{item}" запрещено к использованию, выберите другое')

            if item in description.lower():
                raise forms.ValidationError(f'Слово "{item}" запрещено к использованию, выберите другое')

        return cleaned_data


class BlogForm(forms.ModelForm):
    """
     Создает форму для создания товара
    """

    class Meta:
        """
        Определяет параметры формы
        """
        model = Blog

        fields = ('blog_title', 'blog_text', 'blog_preview')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionForm(forms.ModelForm):
    """
    Создает форму для заполнения даннных версии товара
    """

    ACTIVE_VERSIONS = []  # задаем список активных версий товара

    class Meta:
        model = Version
        # exclude = ('is_active',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """
        Определяет количество активных версий товара
        """
        cleaned_data = super().clean()
        version = self.cleaned_data['is_active']

        if version:
            VersionForm.ACTIVE_VERSIONS.append(True)

        if len(VersionForm.ACTIVE_VERSIONS) > 1:
            print('>1')
            raise forms.ValidationError('Возможна лишь одна активная версия. Пожалуйста, активируйте только 1 версию.')

        return cleaned_data

# class VersionFormSet(BaseInlineFormSet):
#
#     def clean(self):
#         super().clean()
#         current_version = []
#
#         for form in self.forms:
#
#             if form['is_active'].data:
#                 current_version.append(True)
#
#         if len(current_version) > 1:
#             raise forms.ValidationError('Может быть только одна актуальная версия')
