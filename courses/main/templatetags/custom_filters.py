import re
from django import template

register = template.Library()

@register.filter
def convert_images(text):
    """Заменяет [img]...[/img] на HTML <img>"""
    return re.sub(r'\[img\](.*?)\[/img\]', r'<img src="\1" alt="image">', text)