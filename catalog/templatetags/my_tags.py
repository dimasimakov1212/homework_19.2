from django import template

from config import settings

register = template.Library()


@register.filter()
def my_media(value):
    return f"{settings.MEDIA_URL}{value}"
