from django import template

register = template.Library()

@register.simple_tag
def render_stars(rating):
    full_stars = int(rating)
    half_star = rating - full_stars
    empty_stars = 5 - full_stars - (1 if half_star >= 0.5 else 0)
    stars = '★' * full_stars
    if half_star >= 0.5:
        stars += '✬'  # This is a place-holder, you would replace this with an HTML entity or CSS for a half star
    stars += '☆' * empty_stars
    return stars
