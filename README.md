# js_reverse
A Django to use the reverse lookup on the client side via simple javascript function calls.

# [Requirements](https://github.com/OmbraDiFenice/js_reverse/wiki/Installation#requirements)
* Django 1.10
* Python 3.4.5

# [Installation](https://github.com/OmbraDiFenice/js_reverse/wiki/Installation#installation)
To install this app just copy it over in your project, e.g. cloning it directly inside your project root directory:
```sh
~/myproject $ git clone https://github.com/OmbraDiFenice/js_reverse.git
```
and then add it to your project INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'js_reverse',
    ...
]
```
That's it!

# [Quick start](https://github.com/OmbraDiFenice/js_reverse/wiki/Quick-start)
For the impatients. Refer to the [wiki](https://github.com/OmbraDiFenice/js_reverse/wiki) for the [usage details](https://github.com/OmbraDiFenice/js_reverse/wiki/Usage).
```python
# root urls.py
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^someapp/', include('someapp.urls')),
    url(r'^ns_app/', include('ns_app.urls', namespace='nsapp')),
]
```
```python
# someapp urls.py
urlpatterns = [
    url(r'^details/(\d+)/(?<section>.+)/$', views.details, name='details'),
]
```
```python
# ns_app urls.py
urlpatterns = [
    url(r'^list/(?<group>\d+)/$', name='list_group'),
    url(r'^blog/(?<year>[0-9]{4})/(?<month>)0?[1-9]|1[0-2]/(\d+)$', views.article, name='article'),
]
```
```html
<!-- template.html -->
{% load js_reverse %}
<head>
...
{% js_reverse 'nsapp:*' 'index' %}
</head>
<body>
...
<script>
    console.log(Url.reverse('index')); // '/'
    console.log(Url.reverse('details', [12], {section: 'A3'})); // Uncaught URL name "details" not found
    console.log(Url.reverse('nsapp:list_group', {group: '09'})); // '/ns_app/list/09/'
    console.log(Url.reverse('nsapp:article', [10], {year:2016, month: 5})); // '/ns_app/blog/2016/5/10/'
</script>
```

# [Settings](https://github.com/OmbraDiFenice/js_reverse/wiki/Settings)
If you have some name clashes problems you can change the default settigns by specifying these values in your main `settings.py` file:
```python
JS_REVERSE = {
    'ALL_NAMES': '*',
    'JS_OBJECT_NAME': 'Url',
}
```
The values shown above are the default one:
* The very root variable name, `JS_REVERSE`, is the uppercased value of the `name` property in the `js_reverse.apps.JsReverseConfig` _AppConfig_ class
* `ALL_NAMES` the wildcard which allows to select and include all the named views inside a particular namespace
* `JS_OBJECT_NAME` the name of the generated javascript object