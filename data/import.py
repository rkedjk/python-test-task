import sqlite3
import csv
# Создаем или подключаемся к базе данных SQLite
conn = sqlite3.connect("geonames.sqlite")
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS geonames (
        geonameid INTEGER PRIMARY KEY,
        name VARCHAR(200),
        asciiname VARCHAR(200),
        alternatenames VARCHAR(10000),
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6),
        feature_class CHAR(1),
        feature_code VARCHAR(10),
        country_code CHAR(2),
        cc2 VARCHAR(200),
        admin1_code VARCHAR(20),
        admin2_code VARCHAR(80),
        admin3_code VARCHAR(20),
        admin4_code VARCHAR(20),
        population BIGINT,
        elevation INTEGER,
        dem INTEGER,
        timezone VARCHAR(40),
        modification_date DATE)
''')

# Открываем файл и читаем его построчно
with open("data\RU.txt", "r", encoding="utf-8") as file:
    for line in file:
        values = line.strip().split('\t')
        # Добавляем недостающие значения, если необходимо
        while len(values) < 19:
            values.append(None)
        # Преобразуем строки с числовыми значениями
        values[0] = int(values[0])  # geonameid
        values[4] = float(values[4])  # latitude
        values[5] = float(values[5])  # longitude
        values[14] = int(values[14])  # population
        values[15] = int(values[15]) if values[15] else None  # elevation
        values[16] = int(values[16]) if values[16] else None  # dem

        # Вставляем данные в таблицу
        cursor.execute("INSERT INTO geonames VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Данные успешно импортированы в базу данных SQLite.")
