from django import forms

from catalog.models import Product


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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #
    # def clean_email(self):
    #     """
    #     Проверяет корректность ввода email
    #     """
    #     cleaned_data = self.cleaned_data['email']
    #
    #     if 'sky.pro' not in cleaned_data:
    #         raise forms.ValidationError('Почта должна относиться к учебному заведению')
    #
    #     return cleaned_data