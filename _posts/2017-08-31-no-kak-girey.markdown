---
layout: post
title:  Но как гирей...
date:   2017-08-31 16:15:31 +03
tags:   ruby xml html
---

Не понятно, как люди могут пользоваться Питоном, если они когда-либо программировали на Руби. Хотя да. "Не мы такие. Жизнь такая"

Появилась небольшая задачка получить все смс от Ростелекома за текущий год. На телефоне устанавливаем программу SMS Backup and Restore, с помощью которой сохраняем все смски. Сохраняются они в xml.

Для Руби есть библиотека (gem) Nokogiri, предназначенный для работы с HTML и XML.
Вот этот скриптик делает то, что надо:

``` ruby
#!/usr/bin/ruby

require 'nokogiri'

doc = Nokogiri::XML(File.open 'sms.xml')

smses = doc.xpath('smses/sms')                          # 1
  .select {|s| s['address'] == 'Rostelecom'}            # 2
  .map    {|s| s['readable_date'] + "\n" + s['body']}   # 3

puts smses
```

1. Находим все ноды (элементы) с тегом 'sms', которые возвращаются в объекте NodeSet, ведущим себя как массив.

2. Выбираем только те элементы, у которых атрибут 'address' установлен в 'Rostelecom'.

3. Трансформируем ноду в текст из двух строчек, c нужными данными.

Очень здорово, что скрипт пишется также просто, как пишутся конвейеры для шелл - одна задача за раз. Нашел ноды, запустил, глянул, дальше. Отфильтровал, проверил, дальше. Преобразовал - все, готово.
Используем переменные для предотвращения создания громоздких монстров.

Несколько заметок о Nokogiri
-----------------------------

Для памяти.

### Установка в Убунту:

```
sudo apt-get install build-essential patch
sudo apt-get install ruby-dev zlib1g-dev liblzma-dev
sudo -H gem install nokogiri
```

Хм... А libxml2 вроде с gem-ом идет.

### Создание документа

``` ruby
doc = Nokogiri::XML(string)

doc = Nokogiri::HTML(open "FILE")

require 'open-uri'
doc = Nokogiri::HTML(open "URL")

```

### Configuring

http://rdoc.info/github/sparklemotion/nokogiri/Nokogiri/XML/ParseOptions

``` ruby
doc = Nokogiri::XML(File.open("blossom.xml")) do |config|
  config.strict.noblanks
end
```

### Encoding

If you want Nokogiri to handle the document encoding properly, your best bet
is to explicitly set the encoding. Here is an example of explicitly setting
the encoding to EUC-JP on the parser:

doc = Nokogiri.XML('<foo><bar /><foo>', nil, 'EUC-JP')

### Searching

The Node methods xpath and css actually return a NodeSet, which acts very much like an array, and contains matching nodes from the document.

### Single Results

If you know you’re going to get only a single result back, you can use the shortcuts at_css and at_xpath instead of having to access the first element of a NodeSet.

  @doc.css("dramas name").first # => "<name>The A-Team</name>"
  @doc.at_css("dramas name")    # => "<name>The A-Team</name>"

### Namespaces

...

If you have an XML document with namespaces, but would prefer to ignore them
entirely (and query as if Tim Bray had never invented them), then you can call
remove_namespaces! on an XML::Document to remove all namespaces.

### Slop

Maybe you want a more interactive (read: sloppy) way to access nodes and
attributes. If you like what XmlSimple does, then you’ll probably like
Nokogiri’s Slop mode.

### Modifying

Not
