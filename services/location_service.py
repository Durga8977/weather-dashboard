from typing import Optional, Dict, List
from datetime import datetime
from models import Location, CurrentWeather, Forecast, WeatherHistory
from app import db
import logging

logger = logging.getLogger(__name__)

class LocationService:
    """
    Service for managing user locations.
    """
    
    @staticmethod
    def add_location(user_id: int, name: str, latitude: float, longitude: float,
                    country: str = None, timezone: str = None) -> Optional[Location]:
        """
        Add a new location for a user.
        
        Args:
            user_id: User ID
            name: Location name
            latitude: Latitude
            longitude: Longitude
            country: Country name
            timezone: Timezone string
            
        Returns:
            Location object or None
        """
        try:
            location = Location(
                user_id=user_id,
                name=name,
                latitude=latitude,
                longitude=longitude,
                country=country,
                timezone=timezone
            )
            db.session.add(location)
            db.session.commit()
            return location
        except Exception as e:
            logger.error(f"Error adding location: {str(e)}")
            db.session.rollback()
        return None
    
    @staticmethod
    def get_user_locations(user_id: int) -> List[Location]:
        """
        Get all locations for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of Location objects
        """
        return Location.query.filter_by(user_id=user_id).order_by(Location.order).all()
    
    @staticmethod
    def get_location(location_id: int) -> Optional[Location]:
        """
        Get a specific location.
        
        Args:
            location_id: Location ID
            
        Returns:
            Location object or None
        """
        return Location.query.get(location_id)
    
    @staticmethod
    def update_location(location_id: int, **kwargs) -> bool:
        """
        Update location details.
        
        Args:
            location_id: Location ID
            **kwargs: Fields to update
            
        Returns:
            True if successful
        """
        try:
            location = Location.query.get(location_id)
            if not location:
                return False
            
            for key, value in kwargs.items():
                if hasattr(location, key):
                    setattr(location, key, value)
            
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating location: {str(e)}")
            db.session.rollback()
        return False
    
    @staticmethod
    def delete_location(location_id: int) -> bool:
        """
        Delete a location.
        
        Args:
            location_id: Location ID
            
        Returns:
            True if successful
        """
        try:
            location = Location.query.get(location_id)
            if not location:
                return False
            
            db.session.delete(location)
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting location: {str(e)}")
            db.session.rollback()
        return False
    
    @staticmethod
    def set_favorite(location_id: int, is_favorite: bool) -> bool:
        """
        Set location as favorite.
        
        Args:
            location_id: Location ID
            is_favorite: True to favorite, False to unfavorite
            
        Returns:
            True if successful
        """
        return LocationService.update_location(location_id, is_favorite=is_favorite)

class WeatherDataService:
    """
    Service for managing weather data in database.
    """
    
    @staticmethod
    def save_current_weather(location_id: int, weather_data: Dict) -> Optional[CurrentWeather]:
        """
        Save current weather data to database.
        
        Args:
            location_id: Location ID
            weather_data: Parsed weather data
            
        Returns:
            CurrentWeather object or None
        """
        try:
            current = CurrentWeather.query.filter_by(location_id=location_id).first()
            
            if current:
                # Update existing
                for key, value in weather_data.items():
                    if hasattr(current, key):
                        setattr(current, key, value)
            else:
                # Create new
                weather_data['location_id'] = location_id
                current = CurrentWeather(**weather_data)
                db.session.add(current)
            
            db.session.commit()
            return current
        except Exception as e:
            logger.error(f"Error saving current weather: {str(e)}")
            db.session.rollback()
        return None
    
    @staticmethod
    def save_forecast(location_id: int, forecast_list: List[Dict], forecast_type: str = 'daily') -> int:
        """
        Save forecast data to database.
        
        Args:
            location_id: Location ID
            forecast_list: List of forecast items
            forecast_type: 'hourly' or 'daily'
            
        Returns:
            Number of forecasts saved
        """
        try:
            # Clear old forecasts
            Forecast.query.filter_by(location_id=location_id, forecast_type=forecast_type).delete()
            
            count = 0
            for item in forecast_list:
                item['location_id'] = location_id
                item['forecast_type'] = forecast_type
                forecast = Forecast(**item)
                db.session.add(forecast)
                count += 1
            
            db.session.commit()
            return count
        except Exception as e:
            logger.error(f"Error saving forecasts: {str(e)}")
            db.session.rollback()
        return 0
    
    @staticmethod
    def get_current_weather(location_id: int) -> Optional[CurrentWeather]:
        """
        Get current weather for a location.
        
        Args:
            location_id: Location ID
            
        Returns:
            CurrentWeather object or None
        """
        return CurrentWeather.query.filter_by(location_id=location_id).first()
    
    @staticmethod
    def get_forecast(location_id: int, forecast_type: str = 'daily', limit: int = 40) -> List[Forecast]:
        """
        Get forecasts for a location.
        
        Args:
            location_id: Location ID
            forecast_type: 'hourly' or 'daily'
            limit: Maximum number of forecasts
            
        Returns:
            List of Forecast objects
        """
        return Forecast.query.filter_by(
            location_id=location_id,
            forecast_type=forecast_type
        ).order_by(Forecast.forecast_time).limit(limit).all()
