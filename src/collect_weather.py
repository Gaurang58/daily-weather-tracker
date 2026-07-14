import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


LATITUDE = 51.5074
LONGITUDE = -0.1278
LOCATION_NAME = "London"

API_URL = "https://api.open-meteo.com/v1/forecast"

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "weather.csv"


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


def save_weather(current: dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = DATA_FILE.exists()

    row = {
        "collected_at": datetime.now().isoformat(timespec="seconds"),
        "location": LOCATION_NAME,
        "temperature_c": current["temperature_2m"],
        "humidity_percent": current["relative_humidity_2m"],
        "apparent_temperature_c": current["apparent_temperature"],
        "precipitation_mm": current["precipitation"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
    }

    with DATA_FILE.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=row.keys(),
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def main() -> None:
    try:
        weather_data = fetch_weather()
        current = weather_data["current"]

        save_weather(current)

        print(f"Weather saved for {LOCATION_NAME}.")
        print(f"Temperature: {current['temperature_2m']}°C")
        print(f"Data file: {DATA_FILE}")

    except requests.RequestException as error:
        print(f"Unable to fetch weather data: {error}")

    except KeyError as error:
        print(f"Unexpected API response. Missing field: {error}")

    except OSError as error:
        print(f"Unable to save weather data: {error}")


if __name__ == "__main__":
    main()