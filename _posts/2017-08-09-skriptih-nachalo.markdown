---
layout: post
title:  Скрипты. Начало
date:   2017-08-09 17:56:11 +06
tags:   twitter
---

Скопом - по 75 000 (15 раз за 15-минутный интервал, можно и больше - через 15 минут) можно получить идентификаторы следующих пользователей:

* `followers/ids` - читателей любого пользователя, параметр - `user_id` или `screen_name.`
* `friends/ids` - читаемых. Все аналогично followers.

* `blocks/ids` - заблокированных. Можно получить только своих заблокированных пользователей.

* `mutes/users/ids` - непоказываемых. Аналогично blocks.

* `friendships/no_retweets/ids` - непоказываемых ретвиты. Аналогично blocks (почему-то без курсора. А вообще есть такое? В документации небольшой бардак - "Read more about [node:194]" - о строковых id)

* `statuses/retweeters/ids` - третья разновидность, особая и единственная. Список ретвитчиков какого-либо твита.

В общем, не имеет смысла скриптовать последние четыре метода. А к первым двум
надо добавить а) кто меня читает, а я нет - nofriends, б)
кого я читаю, а они нет - nofollowers. Пояснение: nofriends - те, которых нет во friends, но они есть в другом списке, или бы я о них вообще бы не знал. Такая же логика с nofollowers. Также every - и там, и там. Это все в пояснениях - в скрипте получится свой rate limit - 7 раз за 15 минут, и толсто. При необходимости реализация очень проста, что в шелл, что на питоне.

По спискам - надо получать список (эээ... массив) id-шек конкретного списка. И надо добавлять массив id-шек. Поскольку может быть много, то прием со стандартного входа, не c командной строки. Получается:

    tw-ids-followers [USER]
    
    tw-ids-friends   [USER]

    tw-list     LIST
    
    tw-list-add LIST

Скрипты очень простые, основная задача - практика работа с библиотекой. Да, еще, с Twitter API идет консольная утилита, посмотрим, что это такое.

---

Отчет 1. При баловстве с утилитой, идущей в examples/cli.py стало понятно, что это почти `twurl`. Даже лучше, но в "примерах" сидит не зря - сделано на скорую руку. Делать из нее продакшн все-равно не получится, поскольку происходит странная вещь - получается JSON, конвертируется в объект питона, а потом на выход - опять в JSON. 

Убрана рудиментарная поддержка нескольких пользователей (заменена на мой грязный хак), убрана возможность выборки полей из ответа (используем jq) и переименовано в tw. Получилось вот:

    tw -e|-endpoint [-p | -parameter PARAM1=param1 PARAM2=param2...]

Лучше twurl потому, что обработка ошибок (хотя примитивная) и компоновка параметров.

Так что для написания своих скриптов использую шелл, не питон.

---

Вот что оказывается, Петрович. Твиттер в ответ на запрос возвращает один объект. Если возвращаются много объектов, то они помещаются в массив, который присваивается атрибуту возвращаемого объекта. Для получения большего количества объектов, чем допустимо в одном запросе, используется курсор, который передается в следующий запрос. Только для REST интерфейса Twitter API создает свою абстракцию над всем этим - итератор, создаваемый только явно (и это правильно). Итератор создается явно анализируя поля в возвращаемом объекте - а вот это неправильно.

Необходимо скачивать документацию с Твитора, парсить и компилировать в соответствующие метода. Может и сложновато (а может и нет), но всяко реализуемо.

Итог - переписываю `tw` для дополнительного ключа `-i|-iter`, при указании будет возвращаться JSON-массив полученных объектов.

---

Ну вот и бабах об абстракцию. В методе `followers/ids` возвращается объект, в котором есть атрибут `ids`, в котором возвращается 5000 идэшек. При попытке заитерировать это дело с помощью TwitterRestPager - генерируется исключение - int нельзя итерировать. Одного слоя итераторов не хватило. Поэтому в `tweepy` генерировались сначала страницы (pages), а потом итератор по страницам - уже конкретные элементы.

Во общем малой кровью не получилось - моя задумка с консольной утилитой провалилась. Лезть в дебри и исправлять библиотеку не буду, создавать отчет об ошибке тоже - возвращаюсь к написанию скрипта на питоне. Убираю -i из tw.

---

Увяз маленько. Написал только `tw-ids-followers` с самопальной итерацией. 

Этот пост уже перерос. Так что продолжение в следующем. Скорее всего последним на ближайшую пару недель/месяцев. Другие заботы.

