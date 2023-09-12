import sqlite3
from .helpers import get_timezone_difference_hours


class GeoNamesDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        if self.connection:
            self.connection.close()

    def _create_point_dict(self, point_info):
        point_dict = {
            "geonameid": point_info[0],
            "name": point_info[1],
            "asciiname": point_info[2],
            "alternatenames": point_info[3],
            "latitude": point_info[4],
            "longitude": point_info[5],
            "feature_class": point_info[6],
            "feature_code": point_info[7],
            "country_code": point_info[8],
            "cc2": point_info[9],
            "admin1_code": point_info[10],
            "admin2_code": point_info[11],
            "admin3_code": point_info[12],
            "admin4_code": point_info[13],
            "population": point_info[14],
            "elevation": point_info[15],
            "dem": point_info[16],
            "timezone": point_info[17],
            "modification_date": point_info[18],
        }
        return point_dict

    def get_point_info(self, geonameid):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM geonames WHERE geonameid = ?", (geonameid,))
            point_info = cursor.fetchone()

            if point_info:
                point_dict = self._create_point_dict(point_info)
                return point_dict
            else:
                return None
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            self.close()

    def get_points_on_page(self, page_number, points_per_page):
        try:
            self.connect()
            cursor = self.connection.cursor()
            offset = (page_number - 1) * points_per_page
            cursor.execute("SELECT * FROM geonames LIMIT ? OFFSET ?",
                           (points_per_page, offset))
            points_data = cursor.fetchall()

            points_list = []
            for point_info in points_data:
                point_dict = self._create_point_dict(point_info)
                points_list.append(point_dict)

            return points_list
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            self.close()

    def get_point_name_suggestions(self, partial_name):
        try:
            self.connect()
            cursor = self.connection.cursor()

            # Выполняем SQL-запрос для поиска городов, чьи названия начинаются с заданной части
            cursor.execute(
                "SELECT name FROM geonames WHERE name LIKE ? || '%'", (partial_name,))
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
            cursor.execute(
                "SELECT * FROM geonames WHERE alternatenames LIKE ?", ('%' + native_name + '%',))
            point_info = cursor.fetchall()

            if point_info:
                return point_info
            else:
                return {"error": "Point not found with the given native name"}
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        finally:
            self.close()

    def get_prioritized_point(self, point_list):
        try:
            if not point_list:
                return {"error": "point list is empty"}

            # Инициализируем переменные для хранения информации о городе с наибольшим населением
            max_population = 0
            prioritized_point = point_list[0]

            for point_info in point_list:
                # Получаем население текущего города
                population = point_info[14]

                # Если население текущего города больше, чем население ранее выбранного города,
                # обновляем информацию о приоритетном городе
                if population > max_population:
                    max_population = population
                    prioritized_point = point_info

            if prioritized_point:
                return prioritized_point
            else:
                return {"error": "No prioritized point found in the list"}
        except Exception as e:
            print("Error:", e)

    def get_points_timezone_and_northernness_comparison(self, first_point_name_ru, second_point_name_ru):
        try:

            # Получаем информацию о первом городе по русскому названию
            first_point_info = self.get_prioritized_point(
                self.get_point_by_native_name(first_point_name_ru))

            # Получаем информацию о втором городе по русскому названию
            second_point_info = self.get_prioritized_point(
                self.get_point_by_native_name(second_point_name_ru))

            if first_point_info and second_point_info:
                first_point_dict = self._create_point_dict(first_point_info)
                second_point_dict = self._create_point_dict(second_point_info)

                northernness_first = "Northern" if first_point_dict[
                    "latitude"] > second_point_dict["latitude"] else "Southern"
                northernness_second = "Northern" if second_point_dict[
                    "latitude"] > first_point_dict["latitude"] else "Southern"

                timezone_difference = get_timezone_difference_hours(
                    first_point_dict["timezone"], second_point_dict["timezone"])

                return {
                    "first_point": {
                        "timezone": first_point_dict["timezone"],
                        "northernness": northernness_first,
                        "point_info": first_point_dict
                    },
                    "second_point": {
                        "timezone": second_point_dict["timezone"],
                        "northernness": northernness_second,
                        "point_info": second_point_dict
                    },
                    "timezone_difference": timezone_difference
                }

            else:
                return {"error": "One or both points not found in Russia"}
        except sqlite3.Error as e:
            print("Error executing SQL query:", e)
        finally:
            self.close()
