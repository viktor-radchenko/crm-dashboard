from django import template
from django.template.defaulttags import register
from django.conf import settings

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_values(dictionary):
    return dictionary.values()


@register.filter
def get_attr(dictionary, key):
    return getattr(dictionary, key)


@register.filter
def remove_underscore(var):
    return var.replace("_", " ")


@register.filter
def get_getlist(dictionary, key):
    return list(map(int, dictionary.getlist(key)))

@register.filter(name="index_filter")
def index_filter(indexable, i):
    return indexable[i]
