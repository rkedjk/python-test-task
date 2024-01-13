from fastapi import FastAPI
from app.geonames_db import GeoNamesDB
from pathlib import Path

# Determine the base directory for the project
base_dir = Path(__file__).resolve().parent

# Define database file paths
cities_db_path = base_dir / "databases" / "geonames_cities.sqlite"
general_db_path = base_dir / "databases" / "geonames.sqlite"

# Создание экземпляров GeoNamesDB с учетом кросс-платформенности
gndb_city = GeoNamesDB(cities_db_path)
gndb = GeoNamesDB(general_db_path)

# Создаем экземпляр FastAPI сервера
app = FastAPI()

# Обработчик корневого URL
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Обработчик для получения информации о городе по geonameid
@app.get("/city/info/{geonameid}")
def read_city(geonameid: int):
    city_info = gndb_city.get_point_info(geonameid)
    return city_info
# Обработчик для поиска городов по частичному совпадению названия
@app.get("/city/suggest/{partial_name}")
def search_cities(partial_name: str):
    suggestions = gndb_city.get_point_name_suggestions(partial_name)
    return suggestions

# Обработчик для сравнения информации о двух городах
@app.get("/city/compare/{first_city_name}&{second_city_name}")
def compare_cities(first_city_name: str, second_city_name: str):
    comparison = gndb_city.get_points_timezone_and_northernness_comparison(first_city_name, second_city_name)
    return comparison

# Обработчик для получения списка городов на странице
@app.get("/city/listpage/p{page}&q{quantity}")
def cities_page(page: int, quantity: int):
    city_list = gndb_city.get_points_on_page(page, quantity)
    return city_list

# Обработчик для получения информации о точке по geonameid
@app.get("/point/info/{geonameid}")
def read_city(geonameid: int):
    city_info = gndb.get_point_info(geonameid)
    return city_info

# Обработчик для поиска точек по частичному совпадению названия
@app.get("/point/suggest/{partial_name}")
def search_cities(partial_name: str):
    suggestions = gndb.get_point_name_suggestions(partial_name)
    return suggestions

# Обработчик для сравнения информации о двух точках
@app.get("/point/compare/{first_city_name}&{second_city_name}")
def compare_cities(first_city_name: str, second_city_name: str):
    comparison = gndb.get_points_timezone_and_northernness_comparison(first_city_name, second_city_name)
    return comparison

# Обработчик для получения списка точек на странице
@app.get("/point/listpage/p{page}&q{quantity}")
def cities_page(page: int, quantity: int):
    city_list = gndb.get_points_on_page(page, quantity)
    return city_list
