from GeoParser import GoogleEarthLoader, GoogleEarthFormatter

loader = GoogleEarthLoader()

loader.load_data('Data/Jakarta_Highways.geojson')
json_data = loader.normalize()
print(json_data)
print("")

formatter = GoogleEarthFormatter(json_data)
print(formatter.apply_format())