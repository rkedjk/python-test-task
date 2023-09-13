# A class for interacting with a GeoNames SQLite database and performing various queries

import sqlite3
from .helpers import get_timezone_difference_hours

class GeoNamesDB:
    """
    A class for interacting with a GeoNames SQLite database and performing various queries.

    Args:
        db_name (str): The name of the SQLite database file.

    This class provides methods to connect to the database, retrieve information about geographic points,
    perform queries based on point names, calculate time zone differences, and more.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        """
        Close the connection to the database.
        """
        if self.connection:
            self.connection.close()

    def _create_point_dict(self, point_info):
        """
        Create a dictionary from a tuple containing point information.

        Args:
            point_info (tuple): A tuple containing information about a geographic point.

        Returns:
            dict: A dictionary with keys representing point attributes.
        """
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
        """
        Retrieve information about a geographic point by its geonameid.

        Args:
            geonameid (int): The geonameid of the point to retrieve.

        Returns:
            dict or None: A dictionary containing point information or None if the point is not found.
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM geonames WHERE geonameid = ?", (geonameid,))
            point_info = cursor.fetchone()

            if point_info:
                point_dict = self._create_point_dict(point_info)
                return point_dict
            else:
                return None
        except sqlite3.Error as e:
            print("Error executing query:", e)
        finally:
            self.close()

    def get_points_on_page(self, page_number, points_per_page):
        """
        Retrieve a list of geographic points for a specified page and number of points per page.

        Args:
            page_number (int): The page number to retrieve.
            points_per_page (int): The number of points to retrieve per page.

        Returns:
            list: A list of dictionaries, each containing information about a geographic point.
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            offset = (page_number - 1) * points_per_page
            cursor.execute("SELECT * FROM geonames LIMIT ? OFFSET ?", (points_per_page, offset))
            points_data = cursor.fetchall()

            points_list = []
            for point_info in points_data:
                point_dict = self._create_point_dict(point_info)
                points_list.append(point_dict)

            return points_list
        except sqlite3.Error as e:
            print("Error executing query:", e)
        finally:
            self.close()

    def get_point_name_suggestions(self, partial_name):
        """
        Retrieve a list of point name suggestions based on a partial name match.

        Args:
            partial_name (str): The partial name to search for.

        Returns:
            list: A list of suggested point names.
        """
        try:
            self.connect()
            cursor = self.connection.cursor()

            # Execute an SQL query to find cities whose names start with the given partial name
            cursor.execute("SELECT name FROM geonames WHERE name LIKE ? || '%'", (partial_name,))
            suggestions = cursor.fetchall()

            if suggestions:
                suggestion_list = [row[0] for row in suggestions]
                return suggestion_list
            else:
                return []
        except sqlite3.Error as e:
            print("Error executing query:", e)
        finally:
            self.close()

    def get_point_by_native_name(self, native_name):
        """
        Retrieve information about a geographic point by its native name.

        Args:
            native_name (str): The native name of the point to retrieve.

        Returns:
            list or dict: A list of points or an error dictionary if no points are found.
        """
        try:
            self.connect()
            cursor = self.connection.cursor()

            # Execute a query to find points by native name
            cursor.execute("SELECT * FROM geonames WHERE alternatenames LIKE ?", ('%' + native_name + '%',))
            point_info = cursor.fetchall()

            if point_info:
                return point_info
            else:
                return {"error": "Point not found with the given native name"}
        except sqlite3.Error as e:
            print("Error executing query:", e)
        finally:
            self.close()

    def get_prioritized_point(self, point_list):
        """
        Get the point with the highest population from a list of points.

        Args:
            point_list (list): A list of points (dictionaries) to compare.

        Returns:
            dict or dict: The point with the highest population or an error dictionary if the list is empty.
        """
        try:
            if not point_list:
                return {"error": "point list is empty"}

            # Initialize variables to store information about the city with the highest population
            max_population = 0
            prioritized_point = point_list[0]

            for point_info in point_list:
                # Get the population of the current city
                population = point_info[14]

                # If the population of the current city is greater than the previously selected city,
                # update information about the prioritized city
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
        """
        Compare the timezones and northernness of two points based on their Russian names.

        Args:
            first_point_name_ru (str): The Russian name of the first point.
            second_point_name_ru (str): The Russian name of the second point.

        Returns:
            dict or dict: Information about the timezones and northernness comparison of the two points
                          or an error dictionary if one or both points are not found in Russia.
        """
        try:
            # Get information about the first city by its Russian name
            first_point_info = self.get_prioritized_point(
                self.get_point_by_native_name(first_point_name_ru))

            # Get information about the second city by its Russian name
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
            print("Error executing query:", e)
        finally:
            self.close()
