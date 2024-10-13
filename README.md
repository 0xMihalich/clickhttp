# библиотека clickhttp для работы с БД Clickhouse по HTTP-протоколу

## Возможности

* чтение DataFrame на основании SQL-запроса
* выполнение множественного SQL-запроса с возвратом последнего результата как DataFrame
* автоматическое создание временной таблицы с данными на движке MergeTree на основании запроса и возврат ее названия
* insert в таблицу из DataFrame
* поддержка compressed режима работы (сервер принимает и отправляет данные, упакованные в gzip)
* поддержка работы через прокси-сервер
* возможность задать timeout для сессии
* поддержка DataFrame в форматах: dask, numpy, pandas, polars, python, vaex
* инициализация сессии через Airflow connection id либо ручное указание коннектора

## Состав библиотеки

*clickhouse_multiquery*
 — Самостоятельная функция для выполнения множественных запросов к РСУБД Clickhouse без возврата данных.

*ClickHttpSession*
— Класс для работы с Clickhouse по HTTP-протоколу.

*UserConn*
— Объект NamedTuple для создания соединения. Содержит данные для инициализации:

* user      — Тип: str, логин клиента
* password  — Тип: str, пароль клиента
* host      — Тип: str, адрес хоста
* port      — Тип: int, порт для http подключения (при стандартной настройке сервера обычно равен 8123)
* database  — Тип: str, схема в БД (может быть None)

*get_conn*
— Функция для получения объекта UserConn на основании Airflow Connection ID

*ClickHttpError*
— Базовый класс ошибки

*ClosedError*
— Ошибка при попытке выполнить действие после закрытия сессии

*FrameError*
— Ошибка при получении DataFrame

*FrameMultiQueryError*
— Ошибка при выполнении множественного запроса

*InsertError*
— Ошибка при выполнении Isert в таблицу

*FrameType*
— Enum, перечисляющий поддерживаемые типы DataFrame.
  Необходим для определения выходного формата данных для операций чтения при выполнении методов read_frame и send_multiquery.
  Для выбора необходимого типа данных нужно передать в класс параметр frame_type=FrameType.<необходимый тип датафрейм>.
  Так же необходимо понимать, что сама библиотека не устанавливает дополнительные модули и использует те, что пользователь установил самостоятельно.
  При инициализации библиотеки все неустановленные модули будут выведены в warning message с командой для установки.

* dask   — Датафрейм в формате dask.dataframe.DataFrame
* numpy  — Датафрейм в формате numpy.ndarray. Имена колонок отсутствуют
* pandas — Датафрейм в формате pandas.DataFrame
* polars — Датафрейм в формате polars.DataFrame
* python — Вложенный список стандартных объектов python. Имена колонок отсутствуют
* vaex   — Датафрейм в формате vaex.dataframe.DataFrameLocal

*Frame*
— Объект NamedTuple, возвращаемый при выполнении методов read_frame и send_multiquery для класса ClickHttpSession

* columns    — список названий колонок
* types      — список оригинальных типов данных
* data       — DataFrame с данными
* time_read  — время выполнения запроса сервером Clickhouse в мс
* bytes_read — количество байт, отправленных сервером

## Методы класса

    close           — Закрыть сессию. Выполняется при использовании контекстного менеджера with.
    execute         — Выполнить запрос к базе без возвращения результата.
    insert_frame    — Записать данные из DataFrame в таблицу.
    read_frame      — Вернуть результат запроса в виде DataFrame.
    reopen          — Открыть новую сессию. В случае если сессия уже открыта, закроет текущую и откроет новую.
    send_multiquery — Выполнить множественный запрос к БД и вернуть результат последнего запроса как DataFrame.
    set_proxy       — Указать прокси-сервер для соединения. Запуск без параметра удаляет настройку прокси если она ранее была задана.
    temp_query      — На основании запроса создать временную таблицу с данными и вернуть ее название.

## Статические методы, вложенные объекты и атрибуты

    change_mode     — Статический метод. Меняет режим выполнения запросов (сжатие/без сжатия).
    chunk_size      — Атрибут. Размер кусков отправляемого фрейма в байтах, по умолчанию 20мб. Может быть задан при инициализации класса.
    database        — Атрибут. Схема в БД Clickhouse. Значение берется из объекта UserConn либо connection_id Airflow. Задается при инициализации класса.
    frame_type      — Enum-объект FrameType, по умолчанию FrameType.pandas. Задается при инициализации класса FrameType.
    headers         — Заголовки передаваемых запросов. Формируется при инициализации класса, содержит персональные данные.
    is_closed       — Атрибут. Булево, при открытой сессии True.
    is_compressed   — Атрибут. Булево, указывающее на сжатие пакетов для отправки и получения, по умолчанию True. Может быть задан при инициализации класса.
    output_format   — Статический метод. Отображает выбранный метод получения DataFrame от сервера.
    proxy           — Атрибут. Строка адреса прокси-сервера, по умолчанию отсутствует. Может быть задан при инициализации класса.
    session_id      — Атрибут. Уникальный ID текущей сессии как строковое представление UUIDv4. Создается автоматически.
    sess            — Экземпляр класса requests.Session
    timeout         — Атрибут. Время ожидания ответа от сервера в секундах, по умолчанию 10. Может быть задан при инициализации класса.
    url             — Атрибут. Адрес сервера, формируется при инициализации класса.

## Объявленные магические методы класса (без описания)

    __enter__
    __exit__
    __repr__
    __str__

## Installation (Windows/Linux/MacOs)

### Установка из директории

```shell
pip install .
```

### Установка из git

```shell
pip install git+https://github.com/0xMihalich/clickhttp
```

### Установка из pip

```shell
pip install clickhttp
```

## Документация

### Examples

Примеры работы описаны в examples.ipynb

[Скачать файл examples.ipynb по ссылке в google](https://drive.google.com/file/d/1NiZtHW8Nmj1IUBTwmLm8exbkttydhkG5/)

### FAQ

В: Для чего это нужно?

О: В некоторых ETL процессах возникает необходимость в создании нескольких CTE с последующей агрегацией данных в итоговую выборку.
Clickhouse не создает CTE, а каждый раз выполняет один и тот же запрос, объявленный в секции with во всех местах основного запроса,
тратя впустую ресурсы ОЗУ и вычислительные мощности сервера.
Альтернативой CTE может быть временная таблица с данными, при этом Clickhouse не поддерживает выполнение множественных запросов.
Данная библиотека является альтернативой clickhouse-client и clickhouse_driver. Она ни сколько не претендует на звание лучшей,
тем не менее некоторые возможности данного решения могут показаться интересными.
Главная цель библиотеки - выполнение множественных запросов внутри одной сессии, решающее проблему создания Temporary Table с
последующим получением данных.

В: Почему clickhttp.ClickHttpSession не работает в асинхронном режиме, если Clickhouse, как уверяют разработчики, является асинхронным?

О: Хотя сервер Clickhouse выполняет работу в асинхронном режиме, работа внутри одной сессии может быть только синхронной
и задержка между запросами внутри одной сессии не должна превышать более 60 секунд.

В: Почему в файле requirements.txt только backports.zoneinfo и requests? Куда делись numpy, pandas, polars, dask, vaex?

О: Начиная с версии 0.0.5 все импорты, не относящиеся непосредственно к работе Сессия->Запрос | Сессия->Ответ, были исключены
из явных импортов и теперь добавляются только если ранее они были установлены пользователем, поскольку не все пользователи
используют в своей работе все заявленные форматы Dataframe. Кому-то достаточно pandas, кому-то numpy, а кто-то пользуется vaex.
Теперь импорт библиотеки выведет в warning сообщения об отсутствующих компонентах, но продолжит работу.
В случае, если у пользователя нет даже numpy, все получаемые и передаваемые данные будут получены в формате вложенных списков python,
иначе будет возможность выбора типа принимаемого DataFrame, а по умолчанию класс будет инициализирован с типом pandas.DataFrame.

В: Как проверить какие типы датафрейм у меня доступны на данный момент?

О: Вы можете использовать встроенный метод get_names для clickhttp.FrameType. Выполнив данный метод Вы получите список доступных форматов.

В: Установил недостающую библиотеку, но при выполнении clickhttp.FrameType.get_names() ее нет. Что делать?

О: 
```
1. Убедитесь, что библиотека установлена в правильную версию python или в верное виртуальное окружение.
2. Убедитесь, что интерпретатор был перезапущен после установки библиотеки.
3. После выполнения первых двух шагов повторно выполните clickhttp.FrameType.get_names() и убедитесь, что необходимый формат появился.
```

# История версий

## 0.1.0

* Добавлена функция проверки объекта соединения на принадлежность к NamedTuple
* В тесты для workflow добавлена простая проверка работы класса ClickHttpSession
* Для порта 443 добавлено изменение протокола на https
* Функция formatter теперь удаляет лишние пробелы
* В setup.py добавлен url проекта на github

## 0.0.9

* Исправлена проверка объекта connections
* Добавлены простые тесты для workflows
* Исправлена опечатка в CHANGELOG.md

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
