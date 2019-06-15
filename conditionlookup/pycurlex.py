import urllib.request
from django.conf import settings
import json

url = 'https://sheets.googleapis.com/v4/spreadsheets/1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438/values/Cities?key=AIzaSyDamhVUevRxqrvrwT-0bu9iP8LDTK7wRB4'

x = urllib.request.urlopen(url)
jsonData = x.read().decode("utf-8")

cityList = json.loads(jsonData)

print(cityList['values'])
