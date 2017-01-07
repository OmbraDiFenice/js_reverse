if(typeof {{ object_name }} === 'undefined') throw "You need to include js_reverse/object.html first in your page if you want to use add_urls.html file on its own"
{% for name,pattern in patterns.items %}
    {{ object_name }}.patterns['{{ name }}'] = '{{ pattern }}'
{% endfor %}