# FastAPI GeoNames Application

Это приложение FastAPI, предоставляющее API для взаимодействия с базой данных GeoNames. Оно позволяет получать информацию о городах и географических точках, а также выполнять различные сравнения и поиски.

Выполненное техническое задание также доступно на [GitHub](https://github.com/rkedjk/python-test-task)

## Проверка работы приложения 

Кроме локального запуска сервера вы можете использовать следующие ссылки для доступа к API http://94.241.140.165:8000/ и http://rkedjk.duckdns.org:8000/

Интерактивная документация доступна по следующим ссылкам http://94.241.140.165:8000/docs и http://rkedjk.duckdns.org:8000/docs


## Начало работы

Чтобы начать работу с этим приложением, выполните следующие шаги:

1. Клонируйте этот репозиторий на свой локальный компьютер или загрузите архив.

2. Убедитесь что у вас установлен Python 3.11.5, также рекомендуется создать виртуальное окружение venv и выполнять все следующие команды из него. Программа может функционировать на других версиях Python, но полная поддержка не обеспечена.

3. Установите необходимые зависимости, перечисленные в файле `requirements.txt`. Вы можете сделать это с помощью pip:

```bash
pip install -r requirements.txt
```

4.Запустите приложение с использованием предоставленного скрипта:

На Linux/macOS используйте start_bash.sh:
```bash
./start_bash.sh
```
На Windows запустите start_windows.bat, дважды щелкнув по нему или запустив его из командной строки:
```batch
start_windows.bat
```
Если после запуска файлов сервер не включен, запустите его вручную с помощью следующей команды 

```bash
uvicorn main:server --reload
```

После этого сервер должен быть доступен по адресу [127.0.0.1:8000](http://127.0.0.1:8000/) интерактивная документация также доступна http://127.0.0.1:8000/docs
## Особенность 

База данных GeoNames (Конкретно: файл RU.txt) предоставляет данные не только о городах, а обо всех географических названиях России, в следствие этого, такой очевидный запрос как: 

- /city/suggest/Moscow

Выдаст следующий ответ 

``` JSON
[
  "Moscow",
  "Moscow Oblast",
  "Moscow Kremlin",
  "Moscow",
  "Moscow Marriott Hotel Novy Arbat",
  "Moscow Sochi",
  "Moscow Home Hostel",
  "Moscow Good Apartments",
  "Moscow Central",
  "Moscow Orlovo Heliport",
  "Moscow Chkalovskiy Airport",
  "Moscow Chernoye",
  "Moscow Conservatory",
  "Moscow Cottage"
]
```

В следствие этого было реализовано следующее 

- Создана отдельная база данных geonames_cities. В которой содержатся только данные которые имеют feature_code - 'PPL' - "populated place	a city, town, village, or other agglomeration of buildings where people live and work"  
- Данный способ также не идеален, так как не отличает города от других населенных пунктов и регионов. Но для реализации такого необходимо подключать дополнительный внешний источник данных

Поэтому API запросы разделены на два типа 
-  /city/ - для населенных пунктов. Обращается к базе geonames_cities
- /point/ - для всех географических наименований. Обращается к базе geonames

Таким образом для запроса типа point ответ будет следующим

```JSON
[
  "Moscow",
  "Moscow Oblast",
  "Moscow Kremlin",
  "Moscow",
  "Moscow Marriott Hotel Novy Arbat",
  "Moscow Sochi",
  "Moscow Home Hostel",
  "Moscow Good Apartments",
  "Moscow Central",
  "Moscow Orlovo Heliport",
  "Moscow Chkalovskiy Airport",
  "Moscow Chernoye",
  "Moscow Conservatory",
  "Moscow Cottage"
]
```

А для запроса типа city следующим 

```JSON
[
  "Moscow"
]
```
### Почему была создана отдельная база данных а не дополнительная фильтрация внутри программы? 

Многоуровневые конструкции WHERE, значительно увеличат необходимый вычислительный ресурс. В то же время дополнительная база данных занимает вдвое меньшее количество памяти (~ 25МБ против ~50МБ). Поэтому был выбран путь увеличения количества необходимой памяти против увеличения количества вычислительных ресурсов. 

В данном приложении любой подход обеспечил бы примерно одинаковую производительность, ввиду малого размера базы данных, и малого объема программы. Однако я хотел аргументировать свое решение и подход.

## API Endpoints 

Доступны следующие API Запросы.

### city
- /city/info/{geonameid}: Получить информацию о городе по его идентификатору GeoName.

- /city/suggest/{partial_name}: Получить предложения названий городов на основе части имени.

- /city/compare/{first_city_name}&{second_city_name}: Сравнить два города по временным зонам и северности.

- /city/listpage/p{page}&q{quantity}: Получить список городов на указанной странице с указанным количеством.

### point 
- /point/info/{geonameid}: Получить информацию о географической точке по ее идентификатору GeoName.

- /point/suggest/{partial_name}: Получить предложения названий географических точек на основе части имени.

- /point/compare/{first_city_name}&{second_city_name}: Сравнить две географические точки по временным зонам и северности.

- /point/listpage/p{page}&q{quantity}: Получить список географических точек на указанной странице с указанным количеством.

## API DOCS 

## Описание к программному коду и технологиям

### Фреймворки

FastAPI - реализация сервиса REST API 

SQLite - реализация базы данных 

## Класс GeonamesDB

Основной обрабатывающий класс который реализует передачу данных между Web-Сервисом и базой данных

## Описание методов класса GeoNamesDB

### Метод `__init__(self, db_name)`

- Описание: Конструктор класса GeoNamesDB. Инициализирует объект базы данных GeoNames.
- Параметры:
  - `db_name` (str): Имя базы данных, с которой будет работать экземпляр класса.

### Метод `connect(self)`

- Описание: Устанавливает соединение с базой данных.
- Нет параметров.

### Метод `close(self)`

- Описание: Закрывает соединение с базой данных, если оно открыто.
- Нет параметров.

### Метод `_create_point_dict(self, point_info)`

- Описание: Создает словарь с информацией о точке на основе полученных данных из базы данных.
- Параметры:
  - `point_info` (tuple): Кортеж с информацией о точке из базы данных.
- Возвращаемое значение: Словарь с информацией о точке.

### Метод `get_point_info(self, geonameid)`

- Описание: Получает информацию о точке по ее идентификатору GeoName.
- Параметры:
  - `geonameid` (int): Идентификатор GeoName точки.
- Возвращаемое значение: Словарь с информацией о точке или `None`, если точка не найдена.

### Метод `get_points_on_page(self, page_number, points_per_page)`

- Описание: Получает список точек на указанной странице с указанным количеством точек на странице.
- Параметры:
  - `page_number` (int): Номер страницы.
  - `points_per_page` (int): Количество точек на странице.
- Возвращаемое значение: Список словарей с информацией о точках.

### Метод `get_point_name_suggestions(self, partial_name)`

- Описание: Получает предложения названий точек на основе части имени.
- Параметры:
  - `partial_name` (str): Часть имени точки.
- Возвращаемое значение: Список предложений названий точек.

### Метод `get_point_by_native_name(self, native_name)`

- Описание: Получает точку по ее родному названию.
- Параметры:
  - `native_name` (str): Родное название точки.
- Возвращаемое значение: Словарь с информацией о точке или сообщение об ошибке, если точка не найдена.

### Метод `get_prioritized_point(self, point_list)`

- Описание: Получает информацию о точке с наибольшим населением из списка точек.
- Параметры:
  - `point_list` (list): Список словарей с информацией о точках.
- Возвращаемое значение: Словарь с информацией о точке с наибольшим населением или сообщение об ошибке, если список пуст.

### Метод `get_points_timezone_and_northernness_comparison(self, first_point_name_ru, second_point_name_ru)`

- Описание: Сравнивает две точки по временным зонам и северности на основе их русских названий.
- Параметры:
  - `first_point_name_ru` (str): Русское название первой точки.
  - `second_point_name_ru` (str): Русское название второй точки.
- Возвращаемое значение: Словарь с информацией о сравнении двух точек или сообщение об ошибке, если одна или обе точки не найдены.

### Файл helpers.py
