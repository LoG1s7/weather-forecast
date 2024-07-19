from django.urls import path
from forecast.views import city_search_count, weather_view

urlpatterns = [
    path("forecast/", weather_view, name="weather"),
    path(
        "search_count/<str:city>/", city_search_count, name="city_search_count"
    ),
]
