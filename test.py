import geonames_db

your_api_instance = geonames_db.GeoNamesDB("geonames.sqlite")

city_info = your_api_instance.get_city_info(451900)
#print(city_info)
page_number = 2
cities_per_page = 10
city_list = your_api_instance.get_cities_on_page(page_number, cities_per_page)
#print(city_list)
partial_name = "Mos"
suggestions = your_api_instance.get_city_name_suggestions(partial_name)
#print(suggestions)
native_name = "Москва"
point = your_api_instance.get_point_by_native_name(native_name)
#print(point)

priority_city = your_api_instance.get_prioritized_city(city_list)
#print(priority_city) 
first_city_name_ru = "Москва"
second_city_name_ru = "Казань"
comparison_result = your_api_instance.get_cities_timezone_and_northernness_comparison(first_city_name_ru, second_city_name_ru)
print(comparison_result)
