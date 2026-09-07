from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    """User model for storing user accounts and preferences."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    preferences = db.Column(JSON, default={})
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    locations = db.relationship('Location', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    alerts = db.relationship('WeatherAlert', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('FavoriteLocation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Location(db.Model):
    """Model for storing user's saved weather locations."""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    country = db.Column(db.String(80))
    timezone = db.Column(db.String(50))
    is_favorite = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    weather = db.relationship('CurrentWeather', backref='location', lazy='dynamic', cascade='all, delete-orphan')
    forecast = db.relationship('Forecast', backref='location', lazy='dynamic', cascade='all, delete-orphan')
    air_quality = db.relationship('AirQuality', backref='location', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Location {self.name}>'

class CurrentWeather(db.Model):
    """Model for storing current weather data."""
    __tablename__ = 'current_weather'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, index=True)
    temperature = db.Column(db.Float)  # Celsius
    feels_like = db.Column(db.Float)
    humidity = db.Column(db.Integer)  # Percentage
    pressure = db.Column(db.Integer)  # hPa
    wind_speed = db.Column(db.Float)  # m/s
    wind_direction = db.Column(db.Integer)  # degrees
    wind_gust = db.Column(db.Float)
    cloudiness = db.Column(db.Integer)  # Percentage
    precipitation = db.Column(db.Float)  # mm
    visibility = db.Column(db.Float)  # meters
    uv_index = db.Column(db.Float)
    description = db.Column(db.String(255))
    main_condition = db.Column(db.String(50))  # Clear, Clouds, Rain, etc.
    icon = db.Column(db.String(20))  # Weather icon code
    sunrise = db.Column(db.DateTime)
    sunset = db.Column(db.DateTime)
    raw_data = db.Column(JSON)  # Store full API response
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CurrentWeather {self.location_id}: {self.temperature}°C>'

class Forecast(db.Model):
    """Model for storing weather forecast data."""
    __tablename__ = 'forecasts'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, index=True)
    forecast_time = db.Column(db.DateTime, nullable=False, index=True)
    forecast_type = db.Column(db.String(20), nullable=False)  # 'hourly' or 'daily'
    
    # Weather data
    temperature = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.Integer)
    cloudiness = db.Column(db.Integer)
    precipitation = db.Column(db.Float)
    precipitation_probability = db.Column(db.Float)  # Percentage
    description = db.Column(db.String(255))
    main_condition = db.Column(db.String(50))
    icon = db.Column(db.String(20))
    uv_index = db.Column(db.Float)
    
    raw_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Forecast {self.location_id}: {self.forecast_time}>'

class WeatherAlert(db.Model):
    """Model for weather alerts."""
    __tablename__ = 'weather_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)  # 'temp_high', 'temp_low', 'rain', 'wind', 'humidity'
    threshold_value = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    triggered = db.Column(db.Boolean, default=False)
    last_triggered = db.Column(db.DateTime)
    notification_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeatherAlert {self.alert_type}>'

class AirQuality(db.Model):
    """Model for storing air quality data."""
    __tablename__ = 'air_quality'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, index=True)
    aqi = db.Column(db.Integer)  # Air Quality Index (1-5)
    pm2_5 = db.Column(db.Float)  # Fine particles
    pm10 = db.Column(db.Float)   # Particles
    o3 = db.Column(db.Float)     # Ozone
    no2 = db.Column(db.Float)    # Nitrogen dioxide
    so2 = db.Column(db.Float)    # Sulfur dioxide
    co = db.Column(db.Float)     # Carbon monoxide
    quality_level = db.Column(db.String(50))  # Good, Fair, Moderate, Poor, Very Poor
    raw_data = db.Column(JSON)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AirQuality {self.location_id}: AQI {self.aqi}>'

class WeatherHistory(db.Model):
    """Model for storing historical weather data."""
    __tablename__ = 'weather_history'
    
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_avg = db.Column(db.Float)
    humidity_avg = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    wind_speed_avg = db.Column(db.Float)
    description = db.Column(db.String(255))
    main_condition = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<WeatherHistory {self.location_id}: {self.date}>'

class FavoriteLocation(db.Model):
    """Model for favorite locations."""
    __tablename__ = 'favorite_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'location_id', name='unique_user_location'),)
    
    def __repr__(self):
        return f'<FavoriteLocation user_id={self.user_id} location_id={self.location_id}>'
