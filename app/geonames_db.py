import sqlite3

class GeoNamesDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        if self.connection:
            self.connection.close()
    
    def _create_city_dict(self, city_info):
        city_dict = {
            "geonameid": city_info[0],
            "name": city_info[1],
            "asciiname": city_info[2],
            "alternatenames": city_info[3],
            "latitude": city_info[4],
            "longitude": city_info[5],
            "feature_class": city_info[6],
            "feature_code": city_info[7],
            "country_code": city_info[8],
            "cc2": city_info[9],
            "admin1_code": city_info[10],
            "admin2_code": city_info[11],
            "admin3_code": city_info[12],
            "admin4_code": city_info[13],
            "population": city_info[14],
            "elevation": city_info[15],
            "dem": city_info[16],
            "timezone": city_info[17],
            "modification_date": city_info[18],
        }
        return city_dict
            
    def get_city_info(self, geonameid):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM geonames WHERE geonameid = ?", (geonameid,))
            city_info = cursor.fetchone()

            if city_info:
                city_dict = self._create_city_dict(city_info)
                return city_dict
            else:
                return None
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            self.close()

    def get_cities_on_page(self, page_number, cities_per_page):
        try:
            self.connect()
            cursor = self.connection.cursor()
            offset = (page_number - 1) * cities_per_page
            cursor.execute("SELECT * FROM geonames LIMIT ? OFFSET ?", (cities_per_page, offset))
            cities_data = cursor.fetchall()

            cities_list = []
            for city_info in cities_data:
                city_dict = self._create_city_dict(city_info)
                cities_list.append(city_dict)

            return cities_list
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            self.close()

    def get_city_name_suggestions(self, partial_name):
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Выполняем SQL-запрос для поиска городов, чьи названия начинаются с заданной части
            cursor.execute("SELECT name FROM geonames WHERE name LIKE ? || '%'", (partial_name,))
            suggestions = cursor.fetchall()

            if suggestions:
                suggestion_list = [row[0] for row in suggestions]
                return suggestion_list
            else:
                return []
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            self.close()