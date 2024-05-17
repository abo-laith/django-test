# custom_filters.py
from django import template


register = template.Library()

@register.filter(name='remove_trailing_zeros')
def remove_trailing_zeros(decimal_number):
    decimal_str = format(decimal_number, 'f')
    return decimal_str.rstrip('0').rstrip('.') if '.' in decimal_str else decimal_str
