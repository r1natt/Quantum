from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import markdown
import re

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    """ Преобразует Markdown в HTML и заменяет пути картинок. """
    
    static_url = settings.STATIC_URL.rstrip("/")  # Получаем STATIC_URL без лишнего слэша

    # Регулярка для поиска изображений формата ![alt](имя_файла.jpg)
    pattern = r'(!\[.*?\]\()([\w\-.]+\.(jpg|jpeg|png|gif|webp))\)'

    # Заменяем имя файла на полный путь к статике
    text = re.sub(pattern, rf'\1{static_url}/images/lessons/\2)', text)

    # Преобразуем в HTML
    html = markdown.markdown(text)

    return mark_safe(html)