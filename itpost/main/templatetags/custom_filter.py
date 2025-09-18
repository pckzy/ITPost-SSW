from django import template

register = template.Library()

@register.filter
def ends_with(value, arg):
    return value.endswith(arg)

@register.filter
def remove_prefix(value, prefix):
    if value.startswith(prefix):
        return value[len(prefix):]
    return value