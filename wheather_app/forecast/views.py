from datetime import datetime, timedelta

import requests
from django.contrib.auth import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from forecast.models import SearchHistory
from requests.exceptions import RequestException
from rest_framework.decorators import api_view
from rest_framework.response import Response


def get_coordinates(city):
    response = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/"
        f"?apikey={settings.API_KEY}&"
        f"geocode={city}&format=json&lang=ru_RU"
    )
    data = response.json()
    coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"
    ]["Point"]["pos"].split()
    if coordinates:
        return float(coordinates[1]), float(coordinates[0])
    return None, None


def get_weather(lat, lon):
    try:
        start_hour = datetime.now()
        end_hour = start_hour + timedelta(days=3)
        api_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude="
            f"{lat}&longitude={lon}&hourly=temperature_2m,"
            f"relative_humidity_2m,apparent_temperature,"
            f"precipitation_probability,precipitation&"
            f"timezone=Europe%2FMoscow&"
            f"start_hour="
            + start_hour.isoformat(timespec="minutes")
            + "&end_hour="
            + end_hour.isoformat(timespec="minutes")
        )
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except RequestException as e:
        print(f"Произошла ошибка при запросе к API: {e}")
        return None
    except KeyError:
        print("Неверный формат данных полученных от API")
        return None


@login_required
def weather_view(request):
    weather_data = None
    if request.method == "POST":
        city = request.POST.get("city")
        lat, lon = get_coordinates(city)
        if lat and lon:
            data = get_weather(lat, lon)
            hourly = data.get("hourly")
            time = hourly["time"]
            temp = hourly["temperature_2m"]
            relative_humidity = hourly["relative_humidity_2m"]
            apparent_temperature = hourly["apparent_temperature"]
            precipitation_probability = hourly["precipitation_probability"]
            weather_data = tuple(
                zip(
                    time,
                    temp,
                    relative_humidity,
                    apparent_temperature,
                    precipitation_probability,
                )
            )
            # Сохранение истории поиска
            if request.user.is_authenticated:
                history, created = SearchHistory.objects.get_or_create(
                    user=request.user, city=city
                )
                if not created:
                    history.search_count += 1
                    history.save()

    return render(request, "index.html", {"weather_data": weather_data})


@api_view(["GET"])
def city_search_count(request, city):
    search_count = SearchHistory.objects.filter(city=city).count()
    return Response({"city": city, "search_count": search_count})
