#!/usr/bin/env python3
import json
import os
import logging
from typing import List, Dict, Optional

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.cities_file = os.path.join(self.data_dir, 'cities.json')
        self.weather_file = os.path.join(self.data_dir, 'weather_data.json')
        self._ensure_data_file()
        self._ensure_weather_file()
    
    def _ensure_data_file(self):
        if not os.path.exists(self.cities_file):
            with open(self.cities_file, 'w') as f:
                json.dump([], f)
    
    def _ensure_weather_file(self):
        if not os.path.exists(self.weather_file):
            with open(self.weather_file, 'w') as f:
                json.dump({}, f)
    
    def load_cities(self) -> List[str]:
        try:
            with open(self.cities_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading cities: {str(e)}")
            return []
    
    def save_cities(self, cities: List[str]):
        try:
            with open(self.cities_file, 'w') as f:
                json.dump(cities, f)
        except Exception as e:
            self.logger.error(f"Error saving cities: {str(e)}")
    
    def load_weather_data(self) -> Dict:
        try:
            with open(self.weather_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading weather data: {str(e)}")
            return {}
    
    def save_weather_data(self, data: Dict):
        try:
            with open(self.weather_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            self.logger.error(f"Error saving weather data: {str(e)}")
    
    def add_city(self, city: str):
        cities = self.load_cities()
        if city not in cities:
            cities.append(city)
            self.save_cities(cities)
    
    def remove_city(self, city: str):
        cities = self.load_cities()
        if city in cities:
            cities.remove(city)
            self.save_cities(cities)
    
    def update_weather_data(self, city: str, data: Dict):
        weather_data = self.load_weather_data()
        weather_data[city] = data
        self.save_weather_data(weather_data)
