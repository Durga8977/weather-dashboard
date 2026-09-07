import requests
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from flask import current_app
from app import cache
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service for fetching weather data from OpenWeatherMap API.
    """
    
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    AIR_POLLUTION_URL = 'https://api.openweathermap.org/data/2.5/air_pollution'
    
    @staticmethod
    def get_api_key() -> str:
        """Get OpenWeatherMap API key from config."""
        api_key = current_app.config.get('OPENWEATHERMAP_API_KEY')
        if not api_key:
            raise ValueError('OpenWeatherMap API key not configured')
        return api_key
    
    @classmethod
    @cache.cached(timeout=300)  # Cache for 5 minutes
    def get_current_weather(cls, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch current weather data.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Weather data dict or None
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': cls.get_api_key(),
                'units': 'metric'
            }
            response = requests.get(
                f'{cls.BASE_URL}/weather',
                params=params,
                timeout=current_app.config.get('API_REQUEST_TIMEOUT', 10)
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching current weather: {str(e)}")
        return None
    
    @classmethod
    @cache.cached(timeout=3600)  # Cache for 1 hour
    def get_forecast(cls, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch 5-day weather forecast.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Forecast data dict or None
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': cls.get_api_key(),
                'units': 'metric'
            }
            response = requests.get(
                f'{cls.BASE_URL}/forecast',
                params=params,
                timeout=current_app.config.get('API_REQUEST_TIMEOUT', 10)
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching forecast: {str(e)}")
        return None
    
    @classmethod
    @cache.cached(timeout=1800)  # Cache for 30 minutes
    def get_air_quality(cls, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch air quality data.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Air quality data dict or None
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': cls.get_api_key()
            }
            response = requests.get(
                cls.AIR_POLLUTION_URL,
                params=params,
                timeout=current_app.config.get('API_REQUEST_TIMEOUT', 10)
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching air quality: {str(e)}")
        return None
    
    @classmethod
    def geocode_city(cls, city_name: str) -> Optional[Dict]:
        """
        Convert city name to coordinates.
        
        Args:
            city_name: City name (supports 'city,country_code')
            
        Returns:
            Location data with lat/lon or None
        """
        try:
            params = {
                'q': city_name,
                'limit': 1,
                'appid': cls.get_api_key()
            }
            response = requests.get(
                f'{cls.BASE_URL}/find',
                params=params,
                timeout=current_app.config.get('API_REQUEST_TIMEOUT', 10)
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('list'):
                return data['list'][0]
        except requests.RequestException as e:
            logger.error(f"Error geocoding city: {str(e)}")
        return None
    
    @staticmethod
    def parse_weather_response(data: Dict) -> Dict:
        """
        Parse OpenWeatherMap API response into standardized format.
        
        Args:
            data: Raw API response
            
        Returns:
            Parsed weather data
        """
        if not data or 'main' not in data:
            return {}
        
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})
        clouds = data.get('clouds', {})
        rain = data.get('rain', {})
        
        return {
            'temperature': main.get('temp'),
            'feels_like': main.get('feels_like'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'wind_speed': wind.get('speed'),
            'wind_direction': wind.get('deg'),
            'wind_gust': wind.get('gust'),
            'cloudiness': clouds.get('all'),
            'precipitation': rain.get('1h', rain.get('3h')),
            'visibility': data.get('visibility'),
            'description': weather.get('description'),
            'main_condition': weather.get('main'),
            'icon': weather.get('icon'),
            'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise', 0)),
            'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset', 0))
        }
    
    @staticmethod
    def parse_forecast_response(data: Dict) -> List[Dict]:
        """
        Parse forecast API response.
        
        Args:
            data: Raw API response
            
        Returns:
            List of parsed forecast items
        """
        forecasts = []
        for item in data.get('list', []):
            main = item.get('main', {})
            weather = item.get('weather', [{}])[0]
            wind = item.get('wind', {})
            
            forecast = {
                'forecast_time': datetime.fromtimestamp(item.get('dt')),
                'temperature': main.get('temp'),
                'temp_min': main.get('temp_min'),
                'temp_max': main.get('temp_max'),
                'feels_like': main.get('feels_like'),
                'humidity': main.get('humidity'),
                'pressure': main.get('pressure'),
                'wind_speed': wind.get('speed'),
                'wind_direction': wind.get('deg'),
                'cloudiness': item.get('clouds', {}).get('all'),
                'precipitation': item.get('rain', {}).get('3h') or item.get('snow', {}).get('3h'),
                'precipitation_probability': item.get('pop'),
                'description': weather.get('description'),
                'main_condition': weather.get('main'),
                'icon': weather.get('icon')
            }
            forecasts.append(forecast)
        
        return forecasts
