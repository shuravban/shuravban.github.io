---
layout: post
title:  Добавление Google Analytics
date:   2017-08-08 16:31:20 +06
tags:   web jekyll
---

Так. Надо срочно записать мои эксперименты. Github не дает никакого доступа к журналам сайта. Поэтому что-либо узнать об интересе к моему блогу я могу только с помощью сторонних инструментов. Google Analytics - бесплатный, распространенный и настолько продвинутый инструмент, что многие считают, что это его единственный, но очень серьезный недостаток.

Итак [регистрируемся][google-analytics-link]. На странице получаем js-код для отслеживания, который помещаем в специально созданный файл `analytics.html` в папку `_includes`. 

Есть проблема. Когда я тестирую на локальном сервере, все мои обращения с `localhost` также исправно отправляются на сервера Гугл. Чтоб избежать этого, вставляем `analytics.html` в `_layouts/default.html` не просто, а вот так:

{% highlight liquid %}
{% raw %}
{% if jekyll.environment == 'production' %}
  {% include analytics.html %}
{% endif %}
{% endraw %}
{% endhighlight %}

Заодно и как liquid шаблоны в тексте показывать узнал. А билдить перед отправкой на github будем так:

    JEKYLL_ENV=production jekyll build

То есть, естественно, создадим скрипт jb, в котором поместим эту команду.

[google-analytics-link]: https://analytics.google.com/analytics/web/provision?authuser=0#provision/SignUp/

