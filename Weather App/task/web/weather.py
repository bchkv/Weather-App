import requests
from datetime import datetime

API_KEY = "a78f9eaffa1c9564cff63147b153abbe"


class CityNotFoundError(Exception):
    """Exception raised for errors when a city is not found."""


def get_coordinates(city_name):
    """
        Function returns coordinates of the city
    :param city_name:
        The name of the city
    :return:
        Tuple (latitude, longitude)
    :raises:
        CityNotFoundError if the city is not found
    """
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}")
    data = r.json()

    if not data:
        raise CityNotFoundError(city_name)

    data_dict = data[0]
    return data_dict['lat'], data_dict['lon']


def get_weather(city_name, city_id=-1):
    """
    Fetches weather data for provided city.
    :param city_name:
        The name of the city to get weather for
    :param city_id:
        The id of the city taken from the database
    :return:
        Dictionary with data:
        'temperature' — temperature in Celsius
        'time' — time, only an hour value
        'city_name' — city name
        'description' — weather description
        'time_of_day' — time of day: day, evening-morning or night
    :raises:
        CityNotFoundError if city not found
    """
    try:
        lat, lon = get_coordinates(city_name)
    except CityNotFoundError as e:
        raise CityNotFoundError(str(e))

    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    data_dict = r.json()

    time = datetime.utcfromtimestamp(data_dict['dt']).hour
    temperature = data_dict['main']['temp']
    city_name = data_dict['name']
    description = data_dict['weather'][0]['description']
    id = city_id

    if 12 <= time <= 18:
        time_of_day = 'day'
    elif 18 < time < 23 or 6 < time < 12:
        time_of_day = 'evening-morning'
    else:
        time_of_day = 'night'

    return {'id': id, 'time': time, 'time_of_day': time_of_day, 'temperature': temperature, 'city_name': city_name, 'description': description}


if __name__ == '__main__':
    city = input("Enter city name: ")
    print(get_weather(city, 1))