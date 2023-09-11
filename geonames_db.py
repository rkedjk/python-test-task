import sqlite3
import utils

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

    def get_point_by_native_name(self, native_name):
        try:
            self.connect()
            cursor = self.connection.cursor()

            # Выполняем запрос для поиска точки по родному названию
            cursor.execute("SELECT * FROM geonames WHERE alternatenames LIKE ?", ('%' + native_name + '%',))
            point_info = cursor.fetchall()

            if point_info:
                return point_info
            else:
                return {"error": "Point not found with the given native name"}
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        finally:
            self.close()

    def get_prioritized_city(self, city_list):
        try:
            if not city_list:
                return {"error": "City list is empty"}

            # Инициализируем переменные для хранения информации о городе с наибольшим населением
            max_population = 0
            prioritized_city = city_list[0]

            for city_info in city_list:
                # Получаем население текущего города
                population = city_info[14]

                # Если население текущего города больше, чем население ранее выбранного города,
                # обновляем информацию о приоритетном городе
                if population > max_population:
                    max_population = population
                    prioritized_city = city_info

            if prioritized_city:
                return prioritized_city
            else:
                return {"error": "No prioritized city found in the list"}
        except Exception as e:
            print("Error:", e)
        
    def get_cities_timezone_and_northernness_comparison(self, first_city_name_ru, second_city_name_ru):
        try:

            # Получаем информацию о первом городе по русскому названию
            first_city_info = self.get_prioritized_city(self.get_point_by_native_name(first_city_name_ru))

            # Получаем информацию о втором городе по русскому названию
            second_city_info = self.get_prioritized_city(self.get_point_by_native_name(second_city_name_ru))

            if first_city_info and second_city_info:
                first_city_dict = self._create_city_dict(first_city_info)
                second_city_dict = self._create_city_dict(second_city_info)

                northernness_first = "Northern" if first_city_dict["latitude"] > second_city_dict["latitude"] else "Southern"
                northernness_second = "Northern" if second_city_dict["latitude"] > first_city_dict["latitude"] else "Southern"

                timezone_difference = utils.get_timezone_difference_hours(first_city_dict["timezone"],second_city_dict["timezone"])
                
                return {
                    "first_city": {
                        "timezone": first_city_dict["timezone"],
                        "northernness": northernness_first,
                        "city_info": first_city_dict
                    },
                    "second_city": {
                        "timezone": second_city_dict["timezone"],
                        "northernness": northernness_second,
                        "city_info": second_city_dict
                    },
                    "timezone_difference": timezone_difference
                }
                
            else:
                return {"error": "One or both cities not found in Russia"}
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        finally:
            self.close()
