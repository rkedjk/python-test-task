from fastapi import FastAPI, HTTPException
from databases import Database
from app.geonames_db import GeoNamesDB
from pathlib import Path


# Determine the base directory for the project
base_dir = Path(__file__).resolve().parent

# Define database file paths
cities_db_path = base_dir / "databases" / "geonames_cities.sqlite"
general_db_path = base_dir / "databases" / "geonames.sqlite"

# Create instances of GeoNamesDB considering cross-platform compatibility
gndb_city = GeoNamesDB(cities_db_path)
gndb = GeoNamesDB(general_db_path)

# Connect to the databases asynchronously
database_url = "sqlite:///./databases/geonames_cities.sqlite"
database = Database(database_url)

# Create an instance of FastAPI server
app = FastAPI()

# Handler to connect to the database on startup
@app.on_event("startup")
async def startup_db_client():
    await database.connect()

# Handler to disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

# Modify your route handlers to use async functions
@app.get("/city/info/{geonameid}")
async def read_city(geonameid: int):
    city_info = await gndb_city.get_point_info(geonameid, database)
    return city_info

@app.get("/city/suggest/{partial_name}")
async def search_cities(partial_name: str):
    suggestions = await gndb_city.get_point_name_suggestions(partial_name, database)
    return suggestions

# Обработчик для сравнения информации о двух городах
@app.get("/city/compare/{first_city_name}&{second_city_name}")
async def compare_cities(first_city_name: str, second_city_name: str):
    comparison = await gndb_city.get_points_timezone_and_northernness_comparison(first_city_name, second_city_name)
    return comparison

# Обработчик для получения списка городов на странице
@app.get("/city/listpage/p{page}&q{quantity}")
async def cities_page(page: int, quantity: int):
    if page < 1 or quantity < 1:
        raise HTTPException(status_code=400, detail="Invalid parameters")
    
    city_list = await gndb_city.get_points_on_page(page, quantity)
    return city_list

# Обработчик для получения информации о точке по geonameid
@app.get("/point/info/{geonameid}")
async def read_city(geonameid: int):
    city_info = await gndb.get_point_info(geonameid)
    return city_info

# Обработчик для поиска точек по частичному совпадению названия
@app.get("/point/suggest/{partial_name}")
async def search_cities(partial_name: str):
    suggestions = await gndb.get_point_name_suggestions(partial_name)
    return suggestions

# Обработчик для сравнения информации о двух точках
@app.get("/point/compare/{first_city_name}&{second_city_name}")
async def compare_cities(first_city_name: str, second_city_name: str):
    comparison = await gndb.get_points_timezone_and_northernness_comparison(first_city_name, second_city_name)
    return comparison

# Обработчик для получения списка точек на странице
@app.get("/point/listpage/p{page}&q{quantity}")
async def cities_page(page: int, quantity: int):
    city_list = await gndb.get_points_on_page(page, quantity)
    return city_list
