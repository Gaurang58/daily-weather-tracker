from typing import Any

import requests


LATITUDE = 51.5074
LONGITUDE = -0.1278
LOCATION_NAME = "London"

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather() -> dict[str, Any]:
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "weather_code",
        ],
        "timezone": "auto",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


def main() -> None:
    try:
        weather_data = fetch_weather()
        current = weather_data["current"]

        print(f"Location: {LOCATION_NAME}")
        print(f"Temperature: {current['temperature_2m']}°C")
        print(f"Humidity: {current['relative_humidity_2m']}%")
        print(f"Feels like: {current['apparent_temperature']}°C")
        print(f"Precipitation: {current['precipitation']} mm")
        print(f"Wind speed: {current['wind_speed_10m']} km/h")
        print(f"Weather code: {current['weather_code']}")

    except requests.RequestException as error:
        print(f"Unable to fetch weather data: {error}")

    except KeyError as error:
        print(f"Unexpected API response. Missing field: {error}")


if __name__ == "__main__":
    main()