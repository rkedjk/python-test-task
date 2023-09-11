from fastapi import FastAPI
from geonames_db import GeoNamesDB
from utils import *

gndb = GeoNamesDB("geonames.sqlite")

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/city/info/{geonameid}")
def read_city(geonameid: int):
    city_info = gndb.get_city_info(geonameid)
    return city_info

@app.get("/city/suggest/{partial_name}")
def search_cities(partial_name: str):
    suggestions = gndb.get_city_name_suggestions(partial_name)
    return suggestions

@app.get("/city/compare/{first_city_name}&{second_city_name}")
def compare_cities(first_city_name: str, second_city_name: str):
    comparison = gndb.get_cities_timezone_and_northernness_comparison(first_city_name,second_city_name)
    return comparison

@app.get("/city/listpage/p{page}&q{quantity}")
def cities_page(page:int, quantity:int):
    city_list = gndb.get_cities_on_page(page,quantity)
    return city_list