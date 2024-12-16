#!/usr/bin/env python3
from typing import Dict, Optional, Tuple
import logging
import requests

class WeatherAPI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_coordinates(self, city: str) -> Optional[Tuple[float, float]]:
        try:
            params = {
                'name': city,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            
            response = requests.get(self.geocoding_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get('results'):
                result = data['results'][0]
                return result['latitude'], result['longitude']
            return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting coordinates for {city}: {str(e)}")
            return None
    
    def get_current_weather(self, city: str) -> Optional[Dict]:
        try:
            coords = self.get_coordinates(city)
            if not coords:
                return None
                
            lat, lon = coords
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 'weather_code'],
                'timezone': 'auto'
            }
            
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            weather_code = current['weather_code']
            description = self.get_weather_description(weather_code)
            
            return {
                'temperature': round(current['temperature_2m']),
                'humidity': current['relative_humidity_2m'],
                'wind_speed': round(current['wind_speed_10m']),
                'description': description,
                'city_name': city
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching weather for {city}: {str(e)}")
            return None
    
    def get_forecast(self, city: str) -> Optional[Dict]:
        try:
            coords = self.get_coordinates(city)
            if not coords:
                return None
                
            lat, lon = coords
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_probability_mean', 'wind_speed_10m_max', 'weather_code'],
                'timezone': 'auto'
            }
            
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            daily = data['daily']
            
            forecast = []
            for i in range(len(daily['time'])):
                forecast.append({
                    'date': daily['time'][i],
                    'temp_max': round(daily['temperature_2m_max'][i]),
                    'temp_min': round(daily['temperature_2m_min'][i]),
                    'precipitation_prob': daily['precipitation_probability_mean'][i],
                    'wind_speed': round(daily['wind_speed_10m_max'][i]),
                    'description': self.get_weather_description(daily['weather_code'][i])
                })
            
            return forecast
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching forecast for {city}: {str(e)}")
            return None
    
    @staticmethod
    def get_weather_description(code: int) -> str:
        codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return codes.get(code, "Unknown")
