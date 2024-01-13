from collections import namedtuple

# Define a named tuple for point information
PointTuple = namedtuple(
    'PointInfo',
    ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
     'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
     'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
     'dem', 'timezone', 'modification_date']
)
