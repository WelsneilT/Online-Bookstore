from django import template
import random
from django.utils import timezone
register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    return value - arg

@register.filter(name='surrounding_pages')
def surrounding_pages(current_page, num_pages):
    """Returns a range of page numbers around the current page limited by the total number of pages."""
    start = max(current_page - 3, 1)
    end = min(current_page + 3, num_pages)
    return range(start, end + 1)

@register.filter(name='random_order_number')
def random_order_number(value):
    return f"{random.randint(1000, 9999)}"

@register.filter(name='current_time')
def current_time(value):
    return timezone.now()

@register.filter
def custom_range(value):
    if value is None or not isinstance(value, int):
        return range(0)  
    return range(value)