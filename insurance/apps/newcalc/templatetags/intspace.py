from django.utils.encoding import force_unicode
from django import template
import re

register = template.Library()


def intspace(value):
    """
    Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)
intspace.is_safe = True
register.filter(intspace)
