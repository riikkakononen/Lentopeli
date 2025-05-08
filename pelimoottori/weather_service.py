from city_mapping import country_city_map
import requests

API_KEY = "960269c95f971eba44c56ab395ed75d4"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_for_country(country):
    city = country_city_map.get(country, country)

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fi"
    }

    try:
        response = requests.get(BASE_URL, params=params)

        data = response.json()

        weather_main = data["weather"][0]["main"]
        bad_weather = ["Thunderstorm", "Rain", "Snow", "Drizzle"]

        if weather_main in bad_weather:
            return "huono"
        else:
            return "hyvä"

    except Exception as e:
        print(f"Sään hakeminen epäonnistui: {e}")
        # Jos sään hakeminen ei onnistu, valitaan, että sää on hyvä, jotta peli voi jatkua
        return "hyvä"

