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


@register.filter(name="read_it")
def read_it(msg):
    if not msg.is_read:
        msg.is_read = True
        msg.save()


@register.filter(name="get_agency_info")
def get_agency_info(obj):
    return obj.getAgencyInfo()


@register.filter(name="filter_empty_links")
def filter_empty_links(links):
    return [l for l in links if l.link]
