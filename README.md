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

Далее будут описаны примеры API запросов и форматы вывода данных на основе типа /city/

### /city/info/{geonameid}:

#### Формат запроса
```URL
http://127.0.0.1:8000/city/info/524901
```
#### Формат вывода данных 
```JSON
{
    "geonameid": 524901,
    "name": "Moscow",
    "asciiname": "Moscow",
    "alternatenames": "MOW,Maeskuy,Maskav,Maskava,Maskva,Mat-xco-va,Matxcova,Matxcơva,Mosca,Moscfa,Moscha,Mosco,Moscou,Moscova,Moscovo,Moscow,Moscoƿ,Moscu,Moscua,Moscòu,Moscó,Moscù,Moscú,Moskva,Moska,Moskau,Mosko,Moskokh,Moskou,Moskov,Moskova,Moskovu,Moskow,Moskowa,Mosku,Moskuas,Moskva,Moskve,Moskvo,Moskvy,Moskwa,Moszkva,Muskav,Musko,Mát-xcơ-va,Mòskwa,Məskeu,Məskəү,masko,maskw,mo si ke,moseukeuba,mosko,mosukuwa,mskw,mwskva,mwskw,mwsqbh,mx s ko,Μόσχα,Мæскуы,Маскав,Масква,Москва,Москве,Москвы,Москова,Москох,Москъва,Мускав,Муско,Мәскеу,Мәскәү,Մոսկվա,מאָסקװע,מאסקווע,מוסקבה,ماسکو,مسکو,موسكو,موسكۋا,ܡܘܣܩܒܐ,मास्को,मॉस्को,মস্কো,மாஸ்கோ,มอสโก,མོ་སི་ཁོ།,მოსკოვი,ሞስኮ,モスクワ,莫斯科,모스크바",
    "latitude": 55.75222,
    "longitude": 37.61556,
    "feature_class": "P",
    "feature_code": "PPLC",
    "country_code": "RU",
    "cc2": "",
    "admin1_code": "48",
    "admin2_code": "",
    "admin3_code": "",
    "admin4_code": "",
    "population": 10381222,
    "elevation": null,
    "dem": 144,
    "timezone": "Europe/Moscow",
    "modification_date": "2022-12-10"
}

```
### /city/suggest/{partial_name}:

#### Формат запроса
```URL
http://127.0.0.1:8000/city/suggest/Ryazan
```
#### Формат вывода данных 
```JSON
[
  "Ryazanovka",
  "Ryazany",
  "Ryazantsy",
  "Ryazantsy",
  "Ryazantsevo",
  "Ryazantsevo",
  "Ryazantsevo",
  "Ryazanskaya",
  "Ryazanovskiy",
  "Ryazanovskiy",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazankin",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazanka",
  "Ryazan’",
  "Ryazan’",
  "Ryazan’",
  "Ryazanovskaya",
  "Ryazanka",
  "Ryazanskiy",
  "Ryazanki",
  "Ryazantsevla",
  "Ryazan’",
  "Ryazanovo",
  "Ryazanovka",
  "Ryazanovskiye",
  "Ryazanovo",
  "Ryazantsevo",
  "Ryazantsevo",
  "Ryazanskoye",
  "Ryazanovo",
  "Ryazany",
  "Ryazansk",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanovka",
  "Ryazanka",
  "Ryazanovshchina",
  "Ryazanovka",
  "Ryazanovo",
  "Ryazanka",
  "Ryazanovo",
  "Ryazanovshchina",
  "Ryazan’",
  "Ryazanovo",
  "Ryazanovo",
  "Ryazanskiy",
  "Ryazanovo",
  "Ryazanka",
  "Ryazanovo",
  "Ryazanskiy",
  "Ryazanovo",
  "Ryazan’",
  "Ryazanovo"
]
```
### /city/compare/{first_city_name}&{second_city_name}:

#### Формат запроса
```URL
http://127.0.0.1:8000/city/compare/Москва&Калиниград
```
#### Формат вывода данных 
```JSON
{
  "first_point": {
    "timezone": "Europe/Moscow",
    "northernness": "Northern",
    "point_info": {
      "geonameid": 524901,
      "name": "Moscow",
      "asciiname": "Moscow",
      "alternatenames": "MOW,Maeskuy,Maskav,Maskava,Maskva,Mat-xco-va,Matxcova,Matxcơva,Mosca,Moscfa,Moscha,Mosco,Moscou,Moscova,Moscovo,Moscow,Moscoƿ,Moscu,Moscua,Moscòu,Moscó,Moscù,Moscú,Moskva,Moska,Moskau,Mosko,Moskokh,Moskou,Moskov,Moskova,Moskovu,Moskow,Moskowa,Mosku,Moskuas,Moskva,Moskve,Moskvo,Moskvy,Moskwa,Moszkva,Muskav,Musko,Mát-xcơ-va,Mòskwa,Məskeu,Məskəү,masko,maskw,mo si ke,moseukeuba,mosko,mosukuwa,mskw,mwskva,mwskw,mwsqbh,mx s ko,Μόσχα,Мæскуы,Маскав,Масква,Москва,Москве,Москвы,Москова,Москох,Москъва,Мускав,Муско,Мәскеу,Мәскәү,Մոսկվա,מאָסקװע,מאסקווע,מוסקבה,ماسکو,مسکو,موسكو,موسكۋا,ܡܘܣܩܒܐ,मास्को,मॉस्को,মস্কো,மாஸ்கோ,มอสโก,མོ་སི་ཁོ།,მოსკოვი,ሞስኮ,モスクワ,莫斯科,모스크바",
      "latitude": 55.75222,
      "longitude": 37.61556,
      "feature_class": "P",
      "feature_code": "PPLC",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "48",
      "admin2_code": "",
      "admin3_code": "",
      "admin4_code": "",
      "population": 10381222,
      "elevation": null,
      "dem": 144,
      "timezone": "Europe/Moscow",
      "modification_date": "2022-12-10"
    }
  },
  "second_point": {
    "timezone": "Europe/Kaliningrad",
    "northernness": "Southern",
    "point_info": {
      "geonameid": 554234,
      "name": "Kaliningrad",
      "asciiname": "Kaliningrad",
      "alternatenames": "Caliningrado,Calininopolis,KGD,Kalinin'nkrant,Kaliningrad,Kaliningrada,Kaliningradas,Kaliningrado,Kaliningradum,Kaliningrau,Kaliningráu,Kalininqrad,Kalinjingrad,Kalinyingrad,Kalinyingrád,Kalińingrad,Kalíníngrad,Karaliaucios,Karaliaucius,Karaliaučios,Karaliaučius,Kaļiņingrada,Kenisberg,Koenigsbarg,Koenigsberg,Koenigsberg in Preussen,Korigsberg,Krolewiec,Królewiec,Kënisberg,Königsbarg,Königsberg,Königsberg in Preußen,Körigsberg,jia li ning ge lei,kalininagrada,kalliningeuladeu,kalynynghrad,kalynyngrad,kariningurado,qlynyngrd,Καλίνινγκραντ,Калининград,Калињинград,Калінінград,Կալինինգրադ,קלינינגרד,كالينينغراد,کالیننگراڈ,کالینینگراد,کیلننگراڈ,कालिनिनग्राद,ಕಲಿನಿನ್‍ಗ್ರಾಡ್,კალინინგრადი,カリーニングラード,加里寧格勒,칼리닌그라드",
      "latitude": 54.70649,
      "longitude": 20.51095,
      "feature_class": "P",
      "feature_code": "PPLA",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "23",
      "admin2_code": "825118",
      "admin3_code": "",
      "admin4_code": "",
      "population": 475056,
      "elevation": null,
      "dem": 2,
      "timezone": "Europe/Kaliningrad",
      "modification_date": "2023-05-23"
    }
  },
  "timezone_difference": "-1.0"
}
```

### /city/listpage/p{page}&q{quantity}:

#### Формат запроса
```URL
http://127.0.0.1:8000/city/listpage/p5&q3
```
#### Формат вывода данных 
```JSON
[
  {
    "geonameid": 451819,
    "name": "Svoboda",
    "asciiname": "Svoboda",
    "alternatenames": "",
    "latitude": 56.96613,
    "longitude": 34.19721,
    "feature_class": "P",
    "feature_code": "PPL",
    "country_code": "RU",
    "cc2": "",
    "admin1_code": "77",
    "admin2_code": "",
    "admin3_code": "",
    "admin4_code": "",
    "population": 0,
    "elevation": null,
    "dem": 243,
    "timezone": "Europe/Moscow",
    "modification_date": "2011-07-09"
  },
  {
    "geonameid": 451820,
    "name": "Sverchkovo",
    "asciiname": "Sverchkovo",
    "alternatenames": "",
    "latitude": 56.82755,
    "longitude": 34.61065,
    "feature_class": "P",
    "feature_code": "PPL",
    "country_code": "RU",
    "cc2": "",
    "admin1_code": "77",
    "admin2_code": "",
    "admin3_code": "",
    "admin4_code": "",
    "population": 0,
    "elevation": null,
    "dem": 221,
    "timezone": "Europe/Moscow",
    "modification_date": "2011-07-09"
  },
  {
    "geonameid": 451821,
    "name": "Sutoki",
    "asciiname": "Sutoki",
    "alternatenames": "",
    "latitude": 57.17889,
    "longitude": 34.27454,
    "feature_class": "P",
    "feature_code": "PPL",
    "country_code": "RU",
    "cc2": "",
    "admin1_code": "77",
    "admin2_code": "",
    "admin3_code": "",
    "admin4_code": "",
    "population": 0,
    "elevation": null,
    "dem": 219,
    "timezone": "Europe/Moscow",
    "modification_date": "2011-07-09"
  }
]
```
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

Следующая функция вынесена в отдельный модуль, так как использует библиотеку pytz для интерпретации часовых поясов в числовой формат.

### Функция `get_timezone_difference_hours(first_timezone, second_timezone)`

- Описание: Рассчитывает разницу во времени между двумя часовыми поясами и возвращает ее в формате "+X" или "-X".
- Параметры:
  - `first_timezone` (str): Имя первого часового пояса.
  - `second_timezone` (str): Имя второго часового пояса.
- Возвращаемое значение: Разница во времени между двумя часовыми поясами в формате "+X" или "-X", либо "Unknown timezone", если один из часовых поясов неизвестен.

## Описание скрипта импорта данных в базу данных SQLite

### Скрипт `parser.py`

- Описание: Скрипт импорта данных из файла "RU.txt" в базу данных SQLite "geonames_cities.sqlite".
- Импортирует информацию о географических точках в базу данных и создает соответствующую таблицу, если она не существует.

### Шаги скрипта:

1. Подключается к базе данных SQLite с именем "geonames_cities.sqlite" или создает ее, если она не существует.

2. Создает таблицу "geonames" в базе данных, если она не существует. Таблица содержит следующие поля:

   - `geonameid` (INTEGER): Идентификатор GeoName.
   - `name` (VARCHAR(200)): Название точки.
   - `asciiname` (VARCHAR(200)): Транслитерированное название точки.
   - `alternatenames` (VARCHAR(10000)): Альтернативные названия точки.
   - `latitude` (DECIMAL(9, 6)): Широта точки.
   - `longitude` (DECIMAL(9, 6)): Долгота точки.
   - `feature_class` (CHAR(1)): Класс точки.
   - `feature_code` (VARCHAR(10)): Код точки.
   - `country_code` (CHAR(2)): Код страны.
   - `cc2` (VARCHAR(200)): Дополнительные коды страны.
   - `admin1_code` (VARCHAR(20)): Код административной единицы 1-го уровня.
   - `admin2_code` (VARCHAR(80)): Код административной единицы 2-го уровня.
   - `admin3_code` (VARCHAR(20)): Код административной единицы 3-го уровня.
   - `admin4_code` (VARCHAR(20)): Код административной единицы 4-го уровня.
   - `population` (BIGINT): Население точки.
   - `elevation` (INTEGER): Высота над уровнем моря (может быть NULL).
   - `dem` (INTEGER): Модель рельефа (может быть NULL).
   - `timezone` (VARCHAR(40)): Временная зона точки.
   - `modification_date` (DATE): Дата модификации записи.

3. Открывает файл "RU.txt" и читает его построчно.

4. Обрабатывает строки из файла, разделяя их по табуляции и преобразуя значения к соответствующим типам данных.

5. Вставляет данные в таблицу "geonames" базы данных SQLite.

6. Сохраняет изменения и закрывает соединение с базой данных.

7. Выводит сообщение о успешном импорте данных.

### Замечания:

- Скрипт предполагает, что файл "RU.txt" с данными существует в директории "data" и имеет определенный формат.

- Информация о точках, имеющих класс "P" (города), импортируется в базу данных, а остальные данные игнорируются.

- В случае отсутствия значений высоты и модели рельефа в данных, соответствующие поля в базе данных остаются пустыми (NULL).

- Скрипт не предоставляет интерфейса пользователя и выполняет только операции импорта данных.
