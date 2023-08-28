from django import forms

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
    Создает форму для заполнения даннных предмета
    """
    class Meta:
        model = Version
        # exclude = ('is_active',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     super().clean()
    #     active_list = [form.cleaned_data['is_active'] for form in self.forms if 'is_active' in form.cleaned_data]
    #     if active_list.count(True) > 1:
    #         raise ValidationError('Возможна лишь одна активная версия. Пожалуйста, активируйте только 1 версию.')
