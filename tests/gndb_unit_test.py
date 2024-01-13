import sqlite3
import pytest
from app.geonames_db import GeoNamesDB
from pathlib import Path

# Determine the base directory for the project
base_dir = Path(__file__).resolve().parent.parent

# Define database file paths
cities_db_path = base_dir / "databases" / "geonames_cities.sqlite"
general_db_path = base_dir / "databases" / "geonames.sqlite"

# Define a fixture for the mock database
@pytest.fixture
def mock_database(mocker):
    return mocker.Mock(spec=sqlite3.Connection)

def test_get_point_info_exists(mock_database, mocker):
    # Arrange
    geonameid = 1
    mock_cursor = mocker.Mock()
    # Define the behavior to return a tuple
    # Different values for each key
    name_value = 'CityName'
    asciiname_value = 'CityAsciiName'
    alternatenames_value = 'CityAlternateNames'
    latitude_value = 60.28333
    longitude_value = 44.08333
    feature_class_value = 'CityFeatureClass'
    feature_code_value = 'CityFeatureCode'
    country_code_value = 'CityCountryCode'
    cc2_value = 'CityCC2'
    admin1_code_value = 'CityAdmin1Code'
    admin2_code_value = 'CityAdmin2Code'
    admin3_code_value = 'CityAdmin3Code'
    admin4_code_value = 'CityAdmin4Code'
    population_value = 100000
    elevation_value = 500.0
    dem_value = 150
    timezone_value = 'CityTimezone'
    modification_date_value = '2022-01-13'

    mock_cursor.fetchone.side_effect = [
        (
            geonameid, name_value, asciiname_value, alternatenames_value, latitude_value, longitude_value,
            feature_class_value, feature_code_value, country_code_value, cc2_value, admin1_code_value,
            admin2_code_value, admin3_code_value, admin4_code_value, population_value, elevation_value,
            dem_value, timezone_value, modification_date_value
        )
    ]
    mock_database.cursor.return_value = mock_cursor

    # Create a GeoNamesDB instance using the mock database
    geo_db = GeoNamesDB(db_source=mock_database)

    # Act
    result = geo_db.get_point_info(geonameid)

    # Assert
    assert result == {
        'geonameid': 1,
        'name': name_value,
        'asciiname': asciiname_value,
        'alternatenames': alternatenames_value,
        'latitude': latitude_value,
        'longitude': longitude_value,
        'feature_class': feature_class_value,
        'feature_code': feature_code_value,
        'country_code': country_code_value,
        'cc2': cc2_value,
        'admin1_code': admin1_code_value,
        'admin2_code': admin2_code_value,
        'admin3_code': admin3_code_value,
        'admin4_code': admin4_code_value,
        'population': population_value,
        'elevation': elevation_value,
        'dem': dem_value,
        'timezone': timezone_value,
        'modification_date': modification_date_value,
    }


def test_get_point_info_not_exists(mock_database, mocker):
    # Arrange
    geonameid = 123
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = None
    mock_database.cursor.return_value = mock_cursor

    # Create a GeoNamesDB instance using the mock database
    geo_db = GeoNamesDB(db_source=mock_database)

    # Act
    result = geo_db.get_point_info(geonameid)

    # Assert
    assert result is None

def test_get_point_info_invalid_id_type(mock_database, mocker):
    # Arrange
    geonameid = "test"
    mock_cursor = mocker.Mock()
    mock_cursor.fetchone.return_value = None
    mock_database.cursor.return_value = mock_cursor

    # Create a GeoNamesDB instance using the mock database
    geo_db = GeoNamesDB(db_source=mock_database)

    # Act
    result = geo_db.get_point_info(geonameid)

    # Assert
    assert result is None

def test_get_point_info_error_handling(mock_database, mocker):
    # Arrange
    geonameid = 1
    mock_cursor = mocker.Mock()
    mock_cursor.execute.side_effect = sqlite3.Error("Database error")
    mock_database.cursor.return_value = mock_cursor

    # Create a GeoNamesDB instance using the mock database
    geo_db = GeoNamesDB(db_source=mock_database)

    # Act and Assert
    with pytest.raises(sqlite3.Error):
        geo_db.get_point_info(geonameid)
