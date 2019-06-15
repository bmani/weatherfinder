import re
import urllib.request
import json

url = 'https://docs.google.com/spreadsheets/d/1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438/edit?key=AIzaSyDamhVUevRxqrvrwT-0bu9iP8LDTK7wRB4#gid=1015814049'
#url = 'https://docs.google.com/spreadsheets/d/1_Rxr-2jkJgWmmO6xLJJ61SHEXeRCUVIgv6cXXnvz438/edit?usp=sharing'
spreadSheetId = re.search(
    "/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
sheetId = re.search(
    "[#&]gid=([0-9]+)", url)

# print(spreadSheetId.groups()[0])
# print(sheetId.group())

url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyDamhVUevRxqrvrwT-0bu9iP8LDTK7wRB4"

x = urllib.request.urlopen(url)

jsonstr = x.read().decode("utf-8")

print(jsonstr)
