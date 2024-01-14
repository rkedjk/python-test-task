import requests

# Для запуска теста необходимо запустить сервер на localhost

BASE_URL = "http://localhost:8000"

# Тест на получение списка городов
def test_get_city_list():
    response = requests.get(f"{BASE_URL}/city/listpage/p1&q1")
    assert response.status_code == 200
    assert {'admin1_code': '77',
  'admin2_code': '',
  'admin3_code': '',
  'admin4_code': '',
  'alternatenames': '',
  'asciiname': 'Zyabrikovo',
  'cc2': '',
  'country_code': 'RU',
  'dem': 204,
  'elevation': None,
  'feature_class': 'P',
  'feature_code': 'PPL',
  'geonameid': 451747,
  'latitude': 56.84665,
  'longitude': 34.7048,
  'modification_date': '2011-07-09',
  'name': 'Zyabrikovo',
  'population': 0,
  'timezone': 'Europe/Moscow'} in response.json()

# Тест на обработку неверных параметров
def test_invalid_parameters():
    response = requests.get(f"{BASE_URL}/city/listpage/p0&q5")
    assert response.status_code == 400
    assert "Invalid parameters" in response.json()["detail"]

# Тест на обработку неверного формата параметров
def test_invalid_format_parameters():
    response = requests.get(f"{BASE_URL}/city/listpage/pone&q5")
    assert response.status_code == 422
    assert "Invalid parameters" in response.json()["detail"]

# Тест на обработку большого объема данных
def test_large_data():
    response = requests.get(f"{BASE_URL}/city/listpage/p1&q1000")
    assert response.status_code == 200
    assert response.json() != {}

# Тест на отсутствие данных
def test_no_data():
    response = requests.get(f"{BASE_URL}/city/listpage/p100&q10")
    assert response.status_code == 200
    assert "city_list" not in response.json()

# Тест на корректность обработки больших значений параметров
def test_large_parameters():
    response = requests.get(f"{BASE_URL}/city/listpage/p100000&q100")
    assert response.status_code == 200
    assert response.json() != {}
