from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import urllib.request
import json
import re
import sys
import traceback
import urllib.error
from conditionlookup.weatherform import WeatherForm


def index(request):

    resultSet = []
    try:
        if request.method == 'POST':
            form = WeatherForm(request.POST)

            if form.is_valid():
                cityList = getCityListFromGoogleSheet(
                    settings.GOOGLE_SHEET_URL, settings.GOOGLE_API_KEY)
                condition = form.cleaned_data["condition"]
                resultSet = getWeather(cityList, condition)
                print(resultSet)
        else:
            form = WeatherForm()

    except:
        traceback.print_exc(file=sys.stdout)

    print(resultSet)
    return render(request, 'conditionlookup/index.html', {"resultset": resultSet, "form": form})


def getWeather(cityList, condition):
    resultSet = []

    for city in cityList:

        try:
            # If a city is not found, keep going
            omwUrl = settings.OWM_URL.format(
                city[0], "US", settings.OWM_API_KEY)

            x = urllib.request.urlopen(omwUrl)
            omwJson = x.read().decode("utf-8")
            weatherList = json.loads(omwJson)

            coord = weatherList["coord"]

            for weather in weatherList["weather"]:
                # Make sure you the city you are geting is from the same state
                # OWM does not provide State info. So use Google  Reverse GeoCoding

                if findStateForCity(city[1], coord, "administrative_area_level_1") == True:
                    if weather["main"].lower() == condition.lower():
                        resultSet.append(
                            {"city": city[0], "state": city[1], "temperature": round(weatherList["main"]["temp"]), 
                            "wind": round(weatherList["wind"]["speed"])} )

        except:
            print("City:{} has failed OWM lookup".format(city[0]))
            traceback.print_exc(file=sys.stdout)
        #
    return resultSet


def findStateForCity(stateName, latLong, adminLevel):
    # administrative_area_level_1
    try:
        # GeoCode url
        url = settings.GOOGLE_GEOCODE_URL.format(
            latLong["lat"], latLong["lon"], adminLevel, settings.GOOGLE_API_KEY)

        x = urllib.request.urlopen(url)

        jsonData = x.read().decode("utf-8")

        # print(jsonData)
        response = json.loads(jsonData)

        for result in response["results"]:

            # PLEASE MAKE SURE YOU HAVE GEOCODING API WITH BILLING INFO
            # OTHERWISE YOU CAN MAKE API CALL ONLY ONCE..
            # THIS REVERSE GEOCODING TRIES TO GET administrative_area_level_1 (WHICH IS A STATE LEVEL)
            for addComp in result["address_components"]:
                # if the state matches and level matches administrative_area_level_1 then return true
                if(addComp["long_name"] == stateName and adminLevel in addComp["types"]):
                    return True
    except:
        traceback.print_exc(file=sys.stdout)
        return True  # This should not happen, This means this will show all 4 philadelphias

    # I am return True regardless and the Google API returns error because billing info is not entered for API Key
    return True


def getCityListFromGoogleSheet(googleSheetUrl, apiKey):

    cityList = []

    if (googleSheetUrl is None or len(googleSheetUrl) == 0):
        return cityList

    try:

        spreadSheet = re.search(
            "/spreadsheets/d/([a-zA-Z0-9-_]+)", googleSheetUrl)

        spreadSheetId = spreadSheet.groups()[0]

        url = settings.GOOGLE_DOC_URL.format(
            spreadSheetId, settings.GOOGLE_API_KEY)

        x = urllib.request.urlopen(url)
        jsonData = x.read().decode("utf-8")

        resp = json.loads(jsonData)
        cityList = resp["values"]
        del cityList[0]  # remove the header
    except:
        print("Exception in getCityListFromGoogleSheet() ")
        traceback.print_exc(file=sys.stdout)

    return cityList
