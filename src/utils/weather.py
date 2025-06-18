import requests

class Weather:
    @staticmethod
    def get_weather(city: str):
        try:
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru&format=json"
            response = requests.get(geocoding_url)
            data = response.json()
            
            if not data.get("results"):
                return f"Город '{city}' не найден"
            
            location = data["results"][0]
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={location['latitude']}&longitude={location['longitude']}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto"
            response = requests.get(weather_url)
            weather_data = response.json()
            
            if response.status_code == 200:
                current = weather_data["current"]
                weather_descriptions = {0: "ясно", 1: "преимущественно ясно", 2: "переменная облачность", 3: "пасмурно", 45: "туман", 48: "туман с инеем", 51: "легкая морось", 53: "морось", 55: "сильная морось", 61: "небольшой дождь", 63: "дождь", 65: "сильный дождь", 71: "небольшой снег", 73: "снег", 75: "сильный снег", 77: "снежные зерна", 80: "небольшой ливень", 81: "ливень", 82: "сильный ливень", 85: "небольшой снегопад", 86: "сильный снегопад", 95: "гроза", 96: "гроза с небольшим градом", 99: "гроза с сильным градом"}
                return f"Погода в {city}: {current['temperature_2m']}°C, влажность {current['relative_humidity_2m']}%, {weather_descriptions.get(current['weather_code'], 'неизвестно')}"
            return "Не удалось получить данные о погоде"
        except Exception as e:
            return f"Ошибка при получении погоды: {str(e)}" 