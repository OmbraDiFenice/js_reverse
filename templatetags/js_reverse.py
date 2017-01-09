from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.urls.resolvers import RegexURLPattern, RegexURLResolver
from django.urls.exceptions import NoReverseMatch
from django.core.urlresolvers import get_resolver
from django.utils.module_loading import import_string

from collections import OrderedDict

from js_reverse.settings import *

register = template.Library()

def _reverse_all(urlpatterns, partial_name=None, partial_pattern=None, patterns=None):
    partial_name = partial_name if partial_name is not None else ''
    partial_pattern = partial_pattern if partial_pattern is not None else ''
    patterns = patterns if patterns is not None else {}
    for resolver in urlpatterns:
        if isinstance(resolver, RegexURLPattern) and resolver.name:
            patterns[partial_name + resolver.name] = mark_safe('/' + partial_pattern + resolver._regex[1:-1])
        elif isinstance(resolver, RegexURLResolver):
            if resolver.namespace:
                _reverse_all(resolver.url_patterns, partial_name + resolver.namespace + ':', partial_pattern + resolver._regex[1:], patterns)
            else:
                _reverse_all(resolver.url_patterns, partial_name, partial_pattern + resolver._regex[1:], patterns)
    return patterns

def _my_reverse(urlpatterns, path=None, i=None, partial_pattern=None):
    path = path if path is not None else []
    i = i if i is not None else 0
    partial_pattern = partial_pattern if partial_pattern is not None else ''
    
    for resolver in urlpatterns:
        if i == len(path)-1:
            if path[i] == ALL_NAMES:
                partial_name = ':'.join(path[:i])
                if partial_name:
                    partial_name = partial_name + ':'
                return _reverse_all(urlpatterns, partial_name, partial_pattern)
            elif isinstance(resolver, RegexURLPattern) and path[i] == resolver.name:
                return { ':'.join(path): mark_safe('/' + partial_pattern + resolver._regex[1:-1]) }
        elif isinstance(resolver, RegexURLResolver) and path[i] == resolver.namespace:
                return _my_reverse(resolver.url_patterns, path, i+1, partial_pattern + resolver._regex[1:])
    raise NoReverseMatch("Could not find any namespace or view named '%s'" % path[i])

def my_reverse(namespace):
    urlpatterns = import_string(get_resolver(None).urlconf_name + '.urlpatterns')
    path = namespace.split(':')
    return _my_reverse(urlpatterns, path)
    
def build_context(*args, ignoreExceptions=False):
    patterns = {}
    if len(args) == 0:
        args += (ALL_NAMES,)
    for name in args:
        try:
            pattern_list = my_reverse(name)
            for name,pattern in pattern_list.items():
                patterns[name] = pattern
        except NoReverseMatch as e:
            if not ignoreExceptions:
                raise e
            
    return {'patterns': OrderedDict(sorted(patterns.items())), 'object_name': JS_OBJECT_NAME}

@register.inclusion_tag('js_reverse/all.html')
def js_reverse(*args):
    return build_context(*args, ignoreExceptions=True)