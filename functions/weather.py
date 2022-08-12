import httpx
import datetime as dt
from telebot import types
from settings.config import API_KEY


def get_weather(message: types.Message) -> (str, str):
    """Getting weather of the city that user wrote

    :param message: user message with name of the city
    :return: tuple of 2 strings which contains weathe forecast and icon
    """
    try:
        city = message.text
        response = httpx.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}&units=metric').json()

        temp_celsius = response['main']['temp']
        feels_like_celsius = response['main']['feels_like']
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        description = response['weather'][0]['description']
        main_weather = response['weather'][0]['main']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

        icon = response['weather'][0]['icon']
        forecast = (f'***{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}***\n'
                    f'Weather in {city.title()}:\n{main_weather} — {description}\n'
                    f'🌡 {temp_celsius:.2f}°C,\n'
                    f'Feels like: {feels_like_celsius:.2f}°C\n'
                    f'Humidity: {humidity}%\n'
                    f'Wind speed is {wind_speed}m/s\n'
                    f'Sunrise: {sunrise_time}\n'
                    f'Sunset: {sunset_time}')
        return forecast, icon

    except Exception as e:
        print(repr(e))
