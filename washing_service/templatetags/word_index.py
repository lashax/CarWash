from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def nth_word(value: str, n: int) -> str:
    """Returns nth word from a string."""
    return value.split()[n]
