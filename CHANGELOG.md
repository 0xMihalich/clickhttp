# История версий

## 0.0.8

* Добавлено форматирование SQL запроса (с удалением комментариев)
* В requirements.txt добавлена зависимость для сторонней библиотеки sqlparse (форматтер SQL)
* Разрешено использование сторонних объектов NamedTuple для создания объекта connection
* CHUNK_SIZE по умолчанию увеличен до 50 МБ
* Зеркало проекта перенесено на github

## 0.0.7

* Исправлена ошибка отсутствия файла requirements.txt

## 0.0.6

* Некоторые исправления кода
* FAQ.txt и CHANGELOG.md перенесены в README.md
* examples.ipynb загружен на google drive
* Первая публикация пакета в pip

## 0.0.5

* Добавлен FAQ.txt
* Добавлен CHANGELOG.md
* Обновлен README.md
* Обновлен examples.ipynb
* Добавлен необязательный атрибут use_columns для метода insert_table
* Мелкие исправления кода

## 0.0.4

* Версия с предустановленными пакетами dask и vaex перенесена в отдельную ветку
* В requirements.txt оставлена зависимость только от модуля requests
* Формирование объектов DTYPE и FrameType производится динамически в зависимости от установленных пользователем компонентов
* Проведен рефакторинг некоторых функций и методов
* Добавлен метод execute для отправки команд, не требующих возвращения фрейма

## 0.0.3

* Добавлена поддержка dask.dataframe.DataFrame
* Добавлена поддержка vaex.dataframe.DataFrameLocal
* Версия с поддержкой только pandas.DataFrame и polars.DataFrame перенесена в отдельную ветку

## 0.0.2

* Исправлен вывод в лог некоторых сообщений
* Замена logging.warning на logging.info для вывода сообщения при выполнении методов

## 0.0.1

Первая версия библиотеки