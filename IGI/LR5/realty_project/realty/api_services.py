import requests
from decimal import Decimal
from django.core.cache import cache
import logging

logger = logging.getLogger('project')

class CurrencyService:
    """Сервис для получения курсов валют от НБ РБ"""
    BASE_URL = "https://api.nbrb.by/exrates/rates"
    
    @classmethod
    def get_usd_rate(cls):
        """Получить курс USD к BYN"""
        cache_key = 'usd_rate'
        cached_rate = cache.get(cache_key)
        
        if cached_rate:
            return cached_rate
        
        try:
            response = requests.get(f"{cls.BASE_URL}/USD", params={"parammode": "2"})
            response.raise_for_status()
            data = response.json()
            rate = Decimal(str(data['Cur_OfficialRate']))
            
            # Кешируем на 1 час
            cache.set(cache_key, rate, 3600)
            logger.info(f"Получен курс USD: {rate}")
            return rate
        except Exception as e:
            logger.error(f"Ошибка получения курса валют: {e}")
            return Decimal('3.2')  # Значение по умолчанию
    
    @classmethod
    def get_eur_rate(cls):
        """Получить курс EUR к BYN"""
        cache_key = 'eur_rate'
        cached_rate = cache.get(cache_key)
        
        if cached_rate:
            return cached_rate
        
        try:
            response = requests.get(f"{cls.BASE_URL}/EUR", params={"parammode": "2"})
            response.raise_for_status()
            data = response.json()
            rate = Decimal(str(data['Cur_OfficialRate']))
            
            cache.set(cache_key, rate, 3600)
            logger.info(f"Получен курс EUR: {rate}")
            return rate
        except Exception as e:
            logger.error(f"Ошибка получения курса валют: {e}")
            return Decimal('3.5')
    
    @classmethod
    def convert_to_usd(cls, byn_amount):
        """Конвертировать BYN в USD"""
        rate = cls.get_usd_rate()
        return byn_amount / rate
    
    @classmethod
    def convert_to_eur(cls, byn_amount):
        """Конвертировать BYN в EUR"""
        rate = cls.get_eur_rate()
        return byn_amount / rate


class WeatherService:
    """Сервис для получения погоды"""
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    @classmethod
    def get_minsk_weather(cls):
        """Получить текущую погоду в Минске"""
        cache_key = 'minsk_weather'
        cached_weather = cache.get(cache_key)
        
        if cached_weather:
            return cached_weather
        
        try:
            params = {
                'latitude': 53.9,
                'longitude': 27.5667,
                'current_weather': True,
                'hourly': 'temperature_2m,precipitation',
                'timezone': 'Europe/Minsk'
            }
            
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            weather_data = {
                'temperature': data['current_weather']['temperature'],
                'windspeed': data['current_weather']['windspeed'],
                'time': data['current_weather']['time'],
                'weathercode': cls._get_weather_description(data['current_weather']['weathercode'])
            }
            
            # Кешируем на 30 минут
            cache.set(cache_key, weather_data, 1800)
            logger.info(f"Получена погода: {weather_data['temperature']}°C")
            return weather_data
        except Exception as e:
            logger.error(f"Ошибка получения погоды: {e}")
            return {
                'temperature': 20,
                'windspeed': 5,
                'time': 'N/A',
                'weathercode': 'Нет данных'
            }
    
    @staticmethod
    def _get_weather_description(code):
        """Получить описание погоды по коду"""
        weather_codes = {
            0: 'Ясно',
            1: 'В основном ясно',
            2: 'Переменная облачность',
            3: 'Облачно',
            45: 'Туман',
            48: 'Изморозь',
            51: 'Легкая морось',
            53: 'Умеренная морось',
            55: 'Сильная морось',
            61: 'Легкий дождь',
            63: 'Умеренный дождь',
            65: 'Сильный дождь',
            71: 'Легкий снег',
            73: 'Умеренный снег',
            75: 'Сильный снег',
            77: 'Снежные зерна',
            80: 'Легкие ливни',
            81: 'Умеренные ливни',
            82: 'Сильные ливни',
            85: 'Легкий снегопад',
            86: 'Сильный снегопад',
            95: 'Гроза',
            96: 'Гроза с небольшим градом',
            99: 'Гроза с градом'
        }
        return weather_codes.get(code, 'Неизвестно')


class IPGeolocationService:
    """Сервис для определения местоположения по IP"""
    BASE_URL = "http://ip-api.com/json"
    
    @classmethod
    def get_location_by_ip(cls, ip_address=None):
        """Получить информацию о местоположении по IP"""
        cache_key = f'ip_location_{ip_address}' if ip_address else 'ip_location_default'
        cached_location = cache.get(cache_key)
        
        if cached_location:
            return cached_location
        
        try:
            url = f"{cls.BASE_URL}/{ip_address}" if ip_address else cls.BASE_URL
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'success':
                location_data = {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'timezone': data.get('timezone', 'UTC'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'ip': data.get('query', ip_address)
                }
                
                # Кешируем на 1 день
                cache.set(cache_key, location_data, 86400)
                logger.info(f"Получено местоположение для IP {ip_address}: {location_data['city']}, {location_data['country']}")
                return location_data
        except Exception as e:
            logger.error(f"Ошибка получения геолокации: {e}")
        
        return {
            'country': 'Belarus',
            'city': 'Minsk',
            'timezone': 'Europe/Minsk',
            'lat': 53.9,
            'lon': 27.5667,
            'ip': ip_address or 'Unknown'
        }