from django import template

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