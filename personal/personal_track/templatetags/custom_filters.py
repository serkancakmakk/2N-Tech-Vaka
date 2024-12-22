from datetime import datetime
from django import template

register = template.Library()

@register.filter
def get_year_range(value):
    return range(2000, datetime.now().year + 1)

@register.filter
def get_month_range(value):
    return range(1, 13)