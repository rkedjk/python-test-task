import pytest
import sqlite3
from app.geonames_db import GeoNamesDB
from pathlib import Path

# Determine the base directory for the project
base_dir = Path(__file__).resolve().parent.parent.parent

# Define database file paths
cities_db_path = base_dir / "databases" / "geonames_cities.sqlite"

# Создание экземпляров GeoNamesDB с учетом кросс-платформенности
gndb_city = GeoNamesDB(cities_db_path)

def test_get_point_name_suggestions():
    # Test for valid partial name
    suggestions = gndb_city.get_point_name_suggestions("Mosc")
    assert suggestions == ["Moscow"]

def test_get_point_name_suggestions_empty_input():
    # Test when input is an empty string
    suggestions = gndb_city.get_point_name_suggestions("")
    assert suggestions is None

def test_get_point_name_suggestions_no_match():
    # Test when there is no match for the given partial name
    suggestions = gndb_city.get_point_name_suggestions("XYZ")
    assert suggestions is None

def test_get_point_name_suggestions_case_sensitive():
    # Test case sensitivity of the partial name search
    suggestions_upper = gndb_city.get_point_name_suggestions("MOSC")
    suggestions_lower = gndb_city.get_point_name_suggestions("mosc")
    assert suggestions_upper == suggestions_lower


def test_get_point_name_suggestions_special_characters():
    # Test for partial name with special characters
    suggestions = gndb_city.get_point_name_suggestions("Novogusel`skii`")
    assert "Novogusel`skii`" in suggestions
